import math
from abc import abstractmethod

import numpy as np
import shapely

from pysometric.vector import Vector3

from .axis import Axis
from .matrix import rotate_x, rotate_y, rotate_z
from .plane import Plane
from .render import RenderableGeometry, project_point
from .scene import RenderContext
from .texture import Texture
from .vector import Vector2, Vector3


def project_to_plane(point: Vector2, plane: Plane) -> Vector3:
    """Given a point in 2D space, reverse-project it to 3D on the given plane."""
    x, y = point

    if plane == Plane.XY:
        return (x, y, 0)

    if plane == Plane.XZ:
        return (x, 0, y)

    if plane == Plane.YZ:
        return (0, x, y)


def _rotate_vertices_x(
    vertices: list[Vector3], angle: float, center: Vector3
) -> list[Vector3]:
    """Rotates the list of vertices around the X-axis for the given angle with the given center of rotation."""
    return list(map(lambda v: rotate_x(v, angle, center), vertices))


def _rotate_vertices_y(
    vertices: list[Vector3], angle: float, center: Vector3
) -> list[Vector3]:
    return list(map(lambda v: rotate_y(v, angle, center), vertices))


def _rotate_vertices_z(
    vertices: list[Vector3], angle: float, center: Vector3
) -> list[Vector3]:
    return list(map(lambda v: rotate_z(v, angle, center), vertices))


def _regular_polygon_vertices(
    origin: Vector3, num_vertices: int, radius: float, orientation: Plane
) -> list[Vector3]:
    angle = 2 * np.pi / num_vertices
    vertices = []
    for i in range(num_vertices):
        vertices.append((math.cos(i * angle) * radius, math.sin(i * angle) * radius))

    def project_and_translate(v):
        origin_x, origin_y, origin_z = origin
        x, y, z = project_to_plane(v, orientation)
        return (x + origin_x, y + origin_y, z + origin_z)

    vertices = list(map(project_and_translate, vertices))
    return vertices


def _rect_vertices(
    origin: Vector3, width: float, height: float, orientation: Plane
) -> list[Vector3]:
    """Returns the vertices for a rectangular plane with an orientation in the given Plane.

    Vertices will always be returned in clockwise order starting at the origin.
    """
    x, y, z = origin
    hw = width / 2.0
    hh = height / 2.0

    if orientation == Plane.YZ:
        return [
            (x, y - hw, z - hh),
            (x, y + hw, z - hh),
            (x, y + hw, z + hh),
            (x, y - hw, z + hh),
        ]

    if orientation == Plane.XZ:
        return [
            (x - hw, y, z - hh),
            (x - hw, y, z + hh),
            (x + hw, y, z + hh),
            (x + hw, y, z - hh),
        ]

    if orientation == Plane.XY:
        return [
            (x - hw, y - hh, z),
            (x - hw, y + hh, z),
            (x + hw, y + hh, z),
            (x + hw, y - hh, z),
        ]

    raise "Unsupported Plane value provided for orientation."


class Rotation:
    def __init__(self, axis: Axis, angle: float, origin: Vector3):
        self._axis = axis
        self._angle = angle
        self._origin = origin

    @property
    def axis(self):
        return self._axis

    @property
    def angle(self):
        return self._angle

    @property
    def origin(self):
        return self._origin


class Renderable:
    """Base class for all renderable objects, both individual shapes and groups of shapes."""

    def __init__(self, rotations: list[Rotation] = [], layer=1):
        self._layer = layer
        self._rotations = rotations
        self._vertices = []

    @abstractmethod
    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        return []

    @property
    def layer(self) -> int:
        return self._layer

    @property
    def rotations(self) -> list[Rotation]:
        return self._rotations

    @property
    def vertices(self) -> list[Vector3]:
        return self._vertices


class Polygon(Renderable):
    def __init__(
        self,
        vertices: list[Vector3],
        textures: list[Texture] = [],
        rotations: list[Rotation] = [],
        layer=1,
    ):
        super().__init__(rotations, layer)
        self._vertices = vertices
        self._textures = textures
        self._apply_rotations()

    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        polygon2d = shapely.Polygon(
            list(map(lambda v: project_point(v, render_context), self.vertices))
        )
        compiled_textures: list[RenderableGeometry] = [
            texture.compile(polygon2d, render_context) for texture in self.textures
        ]

        return [RenderableGeometry(polygon2d, self._layer)] + compiled_textures

    @property
    def textures(self) -> list[Texture]:
        return self._textures

    def _apply_rotations(self):
        for rotation in self.rotations:
            match rotation.axis:
                case Axis.X:
                    self._vertices = _rotate_vertices_x(
                        self._vertices, rotation.angle, rotation.origin
                    )

                case Axis.Y:
                    self._vertices = _rotate_vertices_y(
                        self._vertices, rotation.angle, rotation.origin
                    )

                case Axis.Z:
                    self._vertices = _rotate_vertices_z(
                        self._vertices, rotation.angle, rotation.origin
                    )


class RegularPolygon(Polygon):
    """Defines a symmetrical polygon in isometric 3D space."""

    def __init__(
        self,
        origin: Vector3,
        num_vertices: int,
        radius: float,
        orientation: Plane,
        textures: list[Texture] = [],
        rotations: list[Rotation] = [],
        layer=1,
    ):
        vertices = _regular_polygon_vertices(origin, num_vertices, radius, orientation)
        super().__init__(vertices, textures, rotations, layer)


class Rectangle(Polygon):
    """Defines a rectangular polygon in 3D space.

    Rectangles should have an orientation parallel to one of the 3 possible
    planes defined in the Plane enumeration.
    """

    def __init__(
        self,
        origin: Vector3,
        width: float,
        height: float,
        orientation: Plane,
        textures: list[Texture] = [],
        rotations: list[Rotation] = [],
        layer=1,
    ):
        super().__init__(
            _rect_vertices(origin, width, height, orientation),
            textures,
            rotations,
            layer,
        )
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class Circle(Polygon):
    def __init__(
        self,
        center: Vector3,
        radius: float,
        orientation: Plane,
        num_segments = 64,
        textures: list[Texture] = [],
        rotations: list[Rotation] = [],
        layer=1,
    ):
        vertices = _regular_polygon_vertices(center, num_segments, radius, orientation)
        super().__init__(vertices, textures, rotations, layer)


class Group:
    def __init__(self, children: list[Renderable]) -> None:
        self._children = children

    @property
    def children(self) -> list[Renderable]:
        return self._children

    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        compiled = []
        for child in self.children:
            compiled = compiled + child.compile(render_context)

        return compiled

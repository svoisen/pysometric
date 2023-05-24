from abc import abstractmethod

import shapely
import numpy as np
import math

from pysometric.vector import Vector3

from .plane import Plane
from .render import RenderableGeometry, project_point
from .scene import RenderContext
from .texture import Texture
from .vector import Vector3, Vector2


def project_to_plane(point: Vector2, plane: Plane) -> Vector3:
    """Given a point in 2D space, reverse-project it to 3D on the given plane."""
    x, y = point

    if plane == Plane.XY:
        return (x, y, 0)

    if plane == Plane.XZ:
        return (x, 0, y)

    if plane == Plane.YZ:
        return (0, x, y)


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
    origin_x, origin_y, origin_z = origin

    if orientation == Plane.YZ:
        return [
            origin,
            (origin_x, origin_y + width, origin_z),
            (origin_x, origin_y + width, origin_z + height),
            (origin_x, origin_y, origin_z + height),
        ]

    if orientation == Plane.XZ:
        return [
            origin,
            (origin_x + width, origin_y, origin_z),
            (origin_x + width, origin_y, origin_z + height),
            (origin_x, origin_y, origin_z + height),
        ]

    if orientation == Plane.XY:
        return [
            origin,
            (origin_x, origin_y + height, origin_z),
            (origin_x + width, origin_y + height, origin_z),
            (origin_x + width, origin_y, origin_z),
        ]

    raise "Unsupported Plane value provided for orientation."


class Shape:
    """Base class for all renderable objects, both individual shapes and groups of shapes."""

    def __init__(self, origin: Vector3, layer=1):
        self.origin = origin
        self.layer = layer

    @abstractmethod
    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        return []


class Polygon(Shape):
    def __init__(self, vertices: list[Vector3] = [], layer=1):
        super().__init__(vertices[0], layer)
        self._vertices = vertices
        self._textures: list[Texture] = []

    @property
    def vertices(self) -> list[Vector3]:
        return self._vertices

    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        polygon2d = shapely.Polygon(
            list(map(lambda v: project_point(v, render_context), self.vertices))
        )
        compiled_textures: list[RenderableGeometry] = [
            texture.compile(polygon2d, render_context) for texture in self.textures
        ]

        return [RenderableGeometry(polygon2d, self.layer)] + compiled_textures

    def add_texture(self, texture: Texture):
        self._textures.append(texture)

    @property
    def textures(self) -> list[Texture]:
        return self._textures


class RegularPolygon(Polygon):
    def __init__(
        self,
        origin: Vector3,
        num_vertices: int,
        radius: float,
        orientation: Plane,
        layer=1,
    ):
        vertices = _regular_polygon_vertices(origin, num_vertices, radius, orientation)
        super().__init__(vertices, layer)


class Rectangle(Polygon):
    """Defines a rectangular polygon in 3D space.

    Rectangles should have an orientation parallel to one of the 3 possible
    planes defined in the Plane enumeration.
    """

    def __init__(
        self, origin: Vector3, width: float, height: float, orientation: Plane, layer=1
    ):
        super().__init__(_rect_vertices(origin, width, height, orientation), layer)
        self._width = width
        self._height = height
        self._orientation = orientation

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def orientation(self):
        return self._orientation


class Group(Shape):
    def __init__(self, children: list[Shape], origin: Vector3, layer=1) -> None:
        super().__init__(origin, layer)
        self._children = children

    @property
    def children(self) -> list[Shape]:
        return self._children

    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        compiled = []
        for child in self.children:
            compiled = compiled + child.compile(render_context)

        return compiled


class Box(Group):
    def __init__(self, origin: Vector3, width=1, depth=1, height=1, layer=1):
        x, y, z = origin
        self.left_plane = Rectangle(origin, depth, height, Plane.YZ, layer)
        self.right_plane = Rectangle(origin, width, height, Plane.XZ, layer)
        self.top_plane = Rectangle((x, y, z + height), width, depth, Plane.XY, layer)

        super().__init__(
            [self.left_plane, self.right_plane, self.top_plane], origin, layer
        )

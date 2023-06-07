from math import radians, sin, cos, sqrt
from .plane import Plane
from .shape import Group, Rectangle, RegularPolygon, Polygon
from .vector import Vector3


class Box(Group):
    def __init__(
        self,
        origin: Vector3,
        width=1,
        depth=1,
        height=1,
        top: dict = {},
        left: dict = {},
        right: dict = {},
    ):
        x, y, z = origin
        hw = width / 2.0
        hd = depth / 2.0
        hh = height / 2.0
        left_plane = Rectangle(
            (x - hw, y, z),
            depth,
            height,
            Plane.YZ,
            left.get("textures") or [],
            [],
            left.get("layer") or 1,
        )
        right_plane = Rectangle(
            (x, y - hd, z),
            width,
            height,
            Plane.XZ,
            right.get("textures") or [],
            [],
            right.get("layer") or 1,
        )
        top_plane = Rectangle(
            (x, y, z + hh),
            width,
            depth,
            Plane.XY,
            top.get("textures") or [],
            [],
            top.get("layer") or 1,
        )

        super().__init__([left_plane, right_plane, top_plane])


class Prism(Group):
    def __init__(self, origin: Vector3, num_sides: int, radius=1, height=1, layer=1) -> None:
        x, y, z = origin
        self._top_face = RegularPolygon((x, y, z + height / 2), num_sides, radius, Plane.XY)
        bottom = RegularPolygon((x, y, z - height / 2), num_sides, radius, Plane.XY)
        faces = []
        faces.append(Polygon([
            self._top_face.vertices[num_sides - 1],
            self._top_face.vertices[0],
            bottom.vertices[0],
            bottom.vertices[num_sides - 1]
        ]))
        for i in range(num_sides - 1):
            vertices = [self._top_face.vertices[i], self._top_face.vertices[i + 1], bottom.vertices[i + 1], bottom.vertices[i]]
            faces.append(Polygon(vertices))
        super().__init__([bottom] + faces + [self._top_face], layer)

    @property
    def top_face(self):
        return self._top_face

    @property
    def bottom_face(self):
        return self._bottom_face

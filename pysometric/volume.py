from functools import cmp_to_key

import shapely

from pysometric.render import RenderableGeometry
from pysometric.scene import RenderContext
from pysometric.shape import Renderable

from .plane import Plane
from .render import RenderableGeometry, project_point
from .shape import Group, Polygon, Rectangle, RegularPolygon
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
    def __init__(
        self,
        origin: Vector3,
        num_sides: int,
        radius=1,
        height=1,
        top={},
        bottom={},
        sides=[],
        rotations=[],
    ) -> None:
        x, y, z = origin
        self._top_face = RegularPolygon(
            (x, y, z + height / 2),
            num_sides,
            radius,
            Plane.XY,
            top.get("textures") or [],
            rotations,
            top.get("layer") or 1,
        )
        self._bottom_face = RegularPolygon(
            (x, y, z - height / 2),
            num_sides,
            radius,
            Plane.XY,
            bottom.get("textures") or [],
            rotations,
            bottom.get("layer") or 1,
        )
        self._side_faces = []
        self._side_faces.append(
            Polygon(
                [
                    self._top_face.vertices[num_sides - 1],
                    self._top_face.vertices[0],
                    self._bottom_face.vertices[0],
                    self._bottom_face.vertices[num_sides - 1],
                ],
                sides[0].get("textures") if len(sides) > 0 else [],
                [],
                sides[0].get("layer") if len(sides) > 0 else 1,
            )
        )
        for i in range(num_sides - 1):
            textures = sides[i + 1].get("textures") if len(sides) > i else []
            layer = sides[i + 1].get("layer") if len(sides) > i else 1
            vertices = [
                self._top_face.vertices[i],
                self._top_face.vertices[i + 1],
                self._bottom_face.vertices[i + 1],
                self._bottom_face.vertices[i],
            ]
            self._side_faces.append(Polygon(vertices, textures, [], layer))

        super().__init__([self._bottom_face] + self._side_faces + [self._top_face])

    @property
    def faces(self):
        return [self._bottom_face] + self._side_faces + [self._top_face]

    @property
    def top_face(self):
        return self._top_face

    @property
    def bottom_face(self):
        return self._bottom_face

    @property
    def side_faces(self):
        return self._side_faces

    def compile(self, render_context: RenderContext) -> list[RenderableGeometry]:
        def zsort(
            p0: tuple[shapely.Polygon, Polygon], p1: tuple[shapely.Polygon, Polygon]
        ):
            # Determine which geometry is visually lower, which means it should be painted first
            _, _, _, ymax0 = shapely.bounds(p0[0])
            _, _, _, ymax1 = shapely.bounds(p1[0])

            if ymax0 < ymax1:
                return -1

            if ymax0 > ymax1:
                return 1

            return 0

        # Sort only sides of the prism based on visual z-order
        sides2d = [
            (
                shapely.Polygon(
                    list(map(lambda v: project_point(v, render_context), side.vertices))
                ),
                side,
            )
            for side in self.side_faces
        ]
        sides_sorted = sorted(sides2d, key=cmp_to_key(zsort))
        self._children = (
            [self._bottom_face]
            + list(map(lambda t: t[1], sides_sorted))
            + [self._top_face]
        )

        return super().compile(render_context)

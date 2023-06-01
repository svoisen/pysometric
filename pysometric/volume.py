from .plane import Plane
from .shape import Group, Rectangle
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
        self.left_plane = Rectangle(
            (x - hw, y, z),
            depth,
            height,
            Plane.YZ,
            left.get("textures") or [],
            [],
            left.get("layer") or 1,
        )
        self.right_plane = Rectangle(
            (x, y - hd, z),
            width,
            height,
            Plane.XZ,
            right.get("textures") or [],
            [],
            right.get("layer") or 1,
        )
        self.top_plane = Rectangle(
            (x, y, z + hh),
            width,
            depth,
            Plane.XY,
            top.get("textures") or [],
            [],
            top.get("layer") or 1,
        )

        super().__init__([self.left_plane, self.right_plane, self.top_plane])

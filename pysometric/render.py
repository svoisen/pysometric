import math

import shapely

from .vector import Vector2, Vector3


class RenderableGeometry:
    """
    Returned by the compile method of any shape to provide information for final rendering.
    A compiled shape includes both the 2D geometry of the shape (projected from 3D) and
    layer information for the shape.
    """

    def __init__(
        self, geometry: shapely.Geometry | shapely.GeometryCollection, layer=1
    ) -> None:
        self.geometry = geometry
        self.layer = layer


class RenderContext:
    """Provides information needed by shapes for compiling and rendering.

    This information is used by the shape's render method to render the shape as a vector drawing.

    Attributes
    ----------
    frame : shapely.Polygon
    grid_pitch : float
    dimetric_angle : float
    origin : Vector2 | str
    """

    def __init__(
        self,
        frame: shapely.Polygon,
        grid_pitch: float,
        dimetric_angle: float,
        origin="centroid",
    ) -> None:
        self.frame = frame
        self.grid_pitch = grid_pitch
        self.dimetric_angle = dimetric_angle
        self._origin = origin

    @property
    def origin(self) -> Vector2:
        """The origin of the grid within the rendering frame."""
        if self._origin == "centroid":
            p = shapely.centroid(self.frame)
            return (p.x, p.y)

        return self._origin


def project_point(point: Vector3, render_context: RenderContext) -> Vector2:
    """
    Given a point in 3D space, project it to 2D screen coordinates.
    """
    origin_x, origin_y = render_context.origin
    grid_pitch = render_context.grid_pitch
    dimetric_angle = render_context.dimetric_angle
    grid_x, grid_y, grid_z = point
    angle_cos = math.cos(dimetric_angle)
    angle_sin = math.sin(dimetric_angle)

    screen_x = (
        origin_x - grid_y * grid_pitch * angle_cos + grid_x * grid_pitch * angle_cos
    )
    screen_y = (
        origin_y
        - grid_y * grid_pitch * angle_sin
        - grid_x * grid_pitch * angle_sin
        - grid_z * grid_pitch
    )

    return (screen_x, screen_y)

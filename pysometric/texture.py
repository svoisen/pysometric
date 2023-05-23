from abc import abstractmethod
from math import radians

import shapely
from vsketch.fill import generate_fill

from .fill import HatchStyle, hatch_fill, line_fill
from .plane import Plane
from .render import RenderContext, RenderableGeometry


class Texture:
    """
    Base class for a texture, which is a 2D skin that can be applied to any Polygon.
    """

    def __init__(self, orientation: Plane, layer=1) -> None:
        self.layer = layer
        self.orientation = orientation

    @abstractmethod
    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        """Compiles the texture for rendering."""


class HatchTexture(Texture):
    """
    A texture that has repeats a hatch (single or cross) fill across the entire polygon
    surface.
    """

    def __init__(
        self,
        orientation: Plane,
        pitch: float,
        style: HatchStyle,
        angle=radians(45),
        inset=0,
        layer=1,
    ) -> None:
        super().__init__(orientation, layer)
        self.pitch = pitch
        self.style = style
        self.angle = angle
        self.inset = inset

    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        fill_clip = polygon2d if self.inset == 0 else polygon2d.buffer(self.inset * -1)
        fill = hatch_fill(fill_clip, self.pitch, self.style, self.angle)
        return RenderableGeometry(fill, self.layer)


class LineTexture(Texture):
    def __init__(self, orientation: Plane, pitch: float, inset=0, layer=1) -> None:
        super().__init__(orientation, layer)
        self.pitch = pitch
        self.inset = inset

    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        fill_clip = polygon2d if self.inset == 0 else polygon2d.buffer(self.inset * -1)
        fill = line_fill(fill_clip, self.pitch)
        return RenderableGeometry(fill, self.layer)


class FillTexture(Texture):
    def __init__(self, orientation: Plane, pen_width=0.5, inset=-0, layer=1) -> None:
        super().__init__(orientation, layer)
        self.pen_width = pen_width
        self.inset = inset

    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        fill_clip = polygon2d if self.inset == 0 else polygon2d.buffer(self.inset * -1)
        fill = generate_fill(fill_clip, self.pen_width, 1.0).as_mls()
        return RenderableGeometry(fill, self.layer)

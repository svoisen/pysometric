from abc import abstractmethod
from math import radians

import shapely
from vsketch.fill import generate_fill

from .fill import hatch_fill
from .render import RenderableGeometry, RenderContext


class Texture:
    """
    Base class for a texture, which is a 2D skin that can be applied to any Polygon.
    """

    def __init__(self, layer=1) -> None:
        self._layer = layer

    @abstractmethod
    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        """Compiles the texture for rendering."""

    @property
    def layer(self) -> int:
        return self._layer


class HatchTexture(Texture):
    """
    A texture that has repeats a hatch (single or cross) fill across the entire polygon
    surface.
    """

    def __init__(
        self,
        pitch: float,
        angle=radians(45),
        inset=0,
        layer=1,
    ) -> None:
        super().__init__(layer)
        self._pitch = pitch
        self._angle = angle
        self._inset = inset

    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        fill_clip = (
            polygon2d if self._inset == 0 else polygon2d.buffer(self._inset * -1)
        )
        fill = hatch_fill(fill_clip, self._pitch, self._angle)
        return RenderableGeometry(fill, self._layer)


class FillTexture(Texture):
    def __init__(self, pen_width=0.5, inset=-0, layer=1) -> None:
        super().__init__(layer)
        self._pen_width = pen_width
        self._inset = inset

    def compile(
        self, polygon2d: shapely.Polygon, render_context: RenderContext
    ) -> RenderableGeometry:
        fill_clip = (
            polygon2d if self._inset == 0 else polygon2d.buffer(self._inset * -1)
        )
        fill = generate_fill(fill_clip, self._pen_width, 1.0).as_mls()
        return RenderableGeometry(fill, self._layer)

from math import radians

import vsketch
from shapely import GeometryCollection, Polygon, STRtree, intersection

from .render import RenderContext
from .shape import RenderableGeometry, Shape

DIMETRIC_ANGLE = radians(30)


class Scene:
    """Defines a 3D isometric scene.

    Scenes may contain zero or more Shape instances describing 3D geometries that can be rendered to 2D.
    """

    def __init__(
        self, frame: Polygon, unit_size: float, origin="centroid", clip_to_frame=True
    ):
        super().__init__()
        self.render_context = RenderContext(frame, unit_size, DIMETRIC_ANGLE, origin)
        self._children: list[Shape] = []
        self.__clips_children_to_frame = clip_to_frame

    def compile(self) -> list[RenderableGeometry]:
        def flatten_compiled(renderables):
            """
            A compiled shape could contain normal Shapely geometries, or a GeometryCollection.
            In the case of a GeometryCollection, flatten it to individual geometries.
            """
            flattened = []
            for renderable in renderables:
                if isinstance(renderable.geometry, GeometryCollection):
                    flattened.extend(
                        list(
                            map(
                                lambda g: RenderableGeometry(g, renderable.layer),
                                renderable.geometry.geoms,
                            )
                        )
                    )
                else:
                    flattened.append(renderable)

            return flattened

        compiled = []
        for child in reversed(self._children):
            clipped_and_compiled = list(
                map(
                    self.__clip_to_frame,
                    flatten_compiled(child.compile(self.render_context)),
                )
            )
            compiled.extend(clipped_and_compiled)

        return self.__occlude(compiled)

    def render(self, vsk: vsketch.Vsketch):
        """Compile and render the scene to the given sketch."""
        renderables = self.compile()
        for renderable in renderables:
            if renderable.layer == 0:
                vsk.noStroke()
            else:
                vsk.stroke(renderable.layer)

            if isinstance(renderable.geometry, list):
                for g in renderable.geometry:
                    vsk.geometry(g)
            else:
                vsk.geometry(renderable.geometry)

    def add(self, child: Shape):
        """Adds a shape to the scene."""
        self._children.append(child)

    @property
    def children(self):
        return self._children

    def __clip_to_frame(self, renderable: RenderableGeometry) -> RenderableGeometry:
        """
        Given a shape, clip it to the scene rendering frame.
        """
        if not self.__clips_children_to_frame:
            return renderable

        renderable.geometry = intersection(
            self.render_context.frame, renderable.geometry
        )
        return renderable

    def __occlude(self, renderables: list[RenderableGeometry]) -> list[RenderableGeometry]:
        geometries = list(map(lambda renderable: renderable.geometry, renderables))
        tree = STRtree(geometries)

        occluded_geometries = renderables
        for i, geometry in enumerate(geometries):
            if not isinstance(geometry, Polygon):
                continue

            intersecting = list(
                filter(
                    lambda idx: idx < i, tree.query(geometry, predicate="intersects")
                )
            )
            for idx in intersecting:
                occluded_geometries[idx].geometry = occluded_geometries[
                    idx
                ].geometry.difference(geometry)

        return occluded_geometries

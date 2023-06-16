import numpy as np
import shapely
import vsketch

import pysometric as pyso


class Example01Sketch(vsketch.SketchClass):
    """
    Creates a grid of boxes with fill and hatch texturing.
    """

    unit_size = vsketch.Param(1.0, unit="cm")

    def create_boxes(self):
        boxes = []
        top = {"textures": [pyso.HatchTexture(4)]}
        right = {"textures": [pyso.FillTexture()]}
        for i in np.arange(-5, 5, 2):
            for j in np.arange(-5, 5, 2):
                boxes.append(pyso.Box((i, j, 0), 1, 1, 1, top, {}, right))

        return boxes

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)

        frame = shapely.box(0, 0, vsk.width, vsk.height)
        scene = pyso.Scene(frame, self.unit_size, self.create_boxes())
        scene.render(vsk)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example01Sketch.display()

import math

import numpy as np
import shapely
import vsketch

import pysometric as psm


class Example03Sketch(vsketch.SketchClass):
    unit_size = vsketch.Param(1.0, unit="cm")
    sphere_radius = vsketch.Param(5.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)
        frame = shapely.box(0, 0, vsk.width, vsk.height)

        circles = []
        for z in np.linspace(self.sphere_radius, -self.sphere_radius, 20):
            circle_radius = math.sqrt(self.sphere_radius * self.sphere_radius - z * z)
            circles.append(psm.Circle((0, 0, z), circle_radius, psm.Plane.XY, 96))

        scene = psm.Scene(frame, self.unit_size, circles)
        scene.render(vsk)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example03Sketch.display()

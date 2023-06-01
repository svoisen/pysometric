import vsketch
import pysometric as pyso
import shapely
import math
import numpy as np

class Example02Sketch(vsketch.SketchClass):
    unit_size = vsketch.Param(0.25, unit="in")
    hexagon_radius = vsketch.Param(1)

    def create_hexagons(self):
        apothem = math.sqrt(3) * self.hexagon_radius / 2
        hexagons = []
        rotation = pyso.Rotation(pyso.Axis.Z, math.radians(90))
        y = 0
        x = 0
        row_count = 0
        while y < 10:
            while x < 10:
                hexagons.append(pyso.RegularPolygon((x, y, 0), 6, self.hexagon_radius, pyso.Plane.XY, [], [rotation]))
                x += apothem * 2
            row_count += 1
            y += self.hexagon_radius * 1.5
            x = -apothem if row_count % 2 != 0 else 0 

        return hexagons

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)
        frame = shapely.box(0, 0, vsk.width, vsk.height)
        scene = pyso.Scene(frame, self.unit_size, self.create_hexagons())
        scene.render(vsk)


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example02Sketch.display()

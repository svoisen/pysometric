import vsketch
import pysometric
import shapely
import math

class Example02Sketch(vsketch.SketchClass):
    unit_size = vsketch.Param(0.25, unit="in")

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)

        frame = shapely.box(0, 0, vsk.width, vsk.height)
        scene = pysometric.Scene(frame, self.unit_size)
        rect = pysometric.Rectangle((0, 0, 0), 1, 1, pysometric.Plane.XY)
        p1 = pysometric.RegularPolygon((0, 0, 0), 6, math.sqrt(2) / 2, pysometric.Plane.XY)
        p2 = pysometric.RegularPolygon((0, 0, -3), 6, math.sqrt(2) / 2, pysometric.Plane.XY)

        scene.add(p1)
        scene.add(p2)
        scene.add(rect)
        scene.render(vsk)


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example02Sketch.display()

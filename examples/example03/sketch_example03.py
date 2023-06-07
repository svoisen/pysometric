import vsketch
import pysometric as psm
import shapely

class Example03Sketch(vsketch.SketchClass):
    width = vsketch.Param(2.0)
    depth = vsketch.Param(2.0)
    unit_size = vsketch.Param(0.25, unit="in")

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)
        frame = shapely.box(0, 0, vsk.width, vsk.height)
        box = psm.Box((0, 0, 0), self.width, self.depth, 1)
        scene = psm.Scene(frame, self.unit_size, [box])
        scene.render(vsk)


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example03Sketch.display()

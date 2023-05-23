import vsketch
import pysometric
import shapely

class Example01Sketch(vsketch.SketchClass):
    unit_size = vsketch.Param(0.25, unit="in")

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)

        frame = shapely.box(0, 0, vsk.width, vsk.height)
        scene = pysometric.Scene(frame, self.unit_size)
        scene.add(pysometric.Box((0, 0, 0)))

        scene.render(vsk)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example01Sketch.display()

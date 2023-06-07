import vsketch
import shapely
import pysometric as psm


class Example04Sketch(vsketch.SketchClass):
    unit_size = vsketch.Param(0.25, unit="in")
    num_sides = vsketch.Param(6, step=1, min_value=3)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)
        prism = psm.Prism((0, 0, 0), self.num_sides, 2, 5)
        scene = psm.Scene(shapely.box(0, 0, vsk.width, vsk.height), self.unit_size, [prism])
        scene.render(vsk)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example04Sketch.display()

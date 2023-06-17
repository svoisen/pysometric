import vsketch
import pysometric as psm
import shapely
import math


class Example03Sketch(vsketch.SketchClass):
    unit_size = vsketch.Param(1.0, unit="cm")

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)
        frame = shapely.box(0, 0, vsk.width, vsk.height)
        cube = psm.Box((0, 0, 0.5), left={"textures": [psm.HatchTexture(3.5)]}, right={"textures": [psm.FillTexture()]})
        pyramid = psm.Pyramid((-1.5, 0, 0), sides=[
            {"textures": [psm.HatchTexture(3.5)]},
            {},
            {},
            {"textures": [psm.FillTexture()]}
        ])
        prism = psm.Prism(
            (1.5, 0, 0.5),
            6,
            0.5,
            sides=[
                {},
                {},
                {},
                {"textures": [psm.HatchTexture(3.5)]},
                {"textures": [psm.FillTexture()]},
                {}
            ]
        )
        scene = psm.Scene(frame, self.unit_size, [pyramid, cube, prism])
        scene.render(vsk)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Example03Sketch.display()

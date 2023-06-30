import pytest
import shapely

from ..scene import Scene, RenderableGeometry
from ..volume import Box

@pytest.fixture
def frame():
    return shapely.box(0, 0, 500, 500)

class TestScene:
    def test_init(self, frame):
        """Test Scene initialization"""
        box = Box((0, 0, 0))
        grid_pitch = 1
        children = [box]
        scene = Scene(frame, grid_pitch, children)

        assert scene.render_context.frame == frame
        assert scene.render_context.grid_pitch == grid_pitch
        assert scene.children == children

    def test_compile(self, frame): 
        """Test Scene.compile()""" 
        box = Box((0, 0, 0)) 
        scene = Scene(frame, 1, [box])
        result = scene.compile()
        assert len(result) == 3 # 3 faces
        assert all([isinstance(r, RenderableGeometry) for r in result])

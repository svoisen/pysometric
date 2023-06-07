import pytest
import shapely

from ..scene import Scene
from ..shape import Rectangle
from ..volume import Box

@pytest.fixture
def frame():
    return shapely.box(0, 0, 500, 500)

class TestScene:
    def test_add(self, frame):
        b = Box((0, 0, 0))
        s = Scene(frame, 100, [b])
        assert len(s.children) == 1
import pytest
import shapely

from ..scene import Scene
from ..shape import Box

@pytest.fixture
def frame():
    return shapely.box(0, 0, 500, 500)

class TestScene:
    def test_add(self, frame):
        s = Scene(frame, 100)
        b = Box((0, 0, 0))
        s.add(b)
        assert len(s.children) == 1

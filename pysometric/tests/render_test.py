import math

import pytest
import shapely

from ..render import RenderContext, project_point
from ..scene import DIMETRIC_ANGLE


@pytest.fixture
def frame():
    return shapely.box(0, 0, 100, 100)


def test_project_point(frame):
    """Test project_point()"""
    render_context = RenderContext(frame, 100, math.radians(DIMETRIC_ANGLE))
    point = (0, 0, 0)
    expected = (50, 50)
    actual = project_point(point, render_context)
    assert expected == actual

    point = (10, 10, 0)
    expected = (50, 31.723)
    actual = project_point(point, render_context)
    assert actual == pytest.approx(expected, 0.001)

import pytest
import numpy as np

from math import radians, sqrt
from ..matrix import rotate_z

def test_rotate_z():
    rotated_point = rotate_z((0, 0, 0), radians(45))
    assert rotated_point == (0, 0, 0)

    rotated_point = rotate_z((0, 1, 0), radians(-90))
    assert rotated_point == pytest.approx((1, 0, 0), 0.01)

    rotated_point = rotate_z((0, 1, 0), radians(180))
    assert rotated_point == pytest.approx((0, -1, 0), 0.01)

    rotated_point = rotate_z((1, 1, 0), radians(90))
    assert rotated_point == pytest.approx((-1, 1, 0), 0.01)

    rotated_point = rotate_z((1, 1, 0), radians(45))
    assert rotated_point == pytest.approx((0, sqrt(2), 0), 0.01)

    rotated_point = rotate_z((1, 1, 0), radians(-45))
    assert rotated_point == pytest.approx((sqrt(2), 0, 0), 0.01)
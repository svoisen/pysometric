import pytest

from ..shape import Circle, Plane, Rectangle, project_to_plane


def test_project_to_plane_xy():
    point = (5, 10)
    expected = (5, 10, 0)
    actual = project_to_plane(point, Plane.XY)
    assert expected == actual


def test_project_to_plane_xz():
    point = (5, 10)
    expected = (5, 0, 10)
    actual = project_to_plane(point, Plane.XZ)
    assert expected == actual


def test_project_to_plane_yz():
    point = (5, 10)
    expected = (0, 5, 10)
    actual = project_to_plane(point, Plane.YZ)
    assert expected == actual


class TestRectangle:
    def test_xy_plane_rectangle_vertices(self):
        expected_vertices = [
            (-0.5, -0.5, 0),
            (-0.5, 0.5, 0),
            (0.5, 0.5, 0),
            (0.5, -0.5, 0),
        ]
        actual = Rectangle((0, 0, 0), 1, 1, Plane.XY).vertices
        assert expected_vertices == actual


class TestCircle:
    def test_circle_vertices(self):
        """Test that a Circle generates the expected number of vertices"""
        circle = Circle((0, 0, 0), 1, Plane.XY, 64)
        assert len(circle.vertices) == 64

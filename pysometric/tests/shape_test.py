import pytest
from ..shape import Plane, Rectangle, project_to_plane, RegularPolygon

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

# def test_yz_plane_rectangle():
#     origin = (0, 0, 0)
#     width = 10
#     height = 8
#     orientation = Plane.YZ
#     expected = [
#         (0, 0, 0),
#         (0, 10, 0),
#         (0, 10, 5),
#         (0, 0, 5)
#     ]
#     actual = Rectangle(origin, width, height, orientation).vertices
#     assert expected == actual

# def test_xz_plane():
#     origin = Vector3(0, 0, 0)
#     width = 10
#     height = 5
#     orientation = Plane.XZ
#     expected = [
#         Vector3(0, 0, 0),
#         Vector3(10, 0, 0),
#         Vector3(10, 0, 5),
#         Vector3(0, 0, 5)
#     ]
#     actual = _rect_vertices(origin, width, height, orientation)
#     assert expected == actual

# def test_xy_plane():
#     origin = Vector3(0, 0, 0)
#     width = 10
#     height = 5
#     orientation = Plane.XY
#     expected = [
#         Vector3(0, 0, 0),
#         Vector3(0, 5, 0),
#         Vector3(10, 5, 0),
#         Vector3(10, 0, 0)
#     ]
#     actual = _rect_vertices(origin, width, height, orientation)
#     assert expected == actual 

# def test_regular_polygon():
#     origin = (0, 0, 0)
#     polygon = RegularPolygon(origin, 3, 10, Plane.XY)
#     expected_vertices = [
#         (10.0, 0, 0),
#         (0, 0, 0),
#         (0, 0, 0)
#     ]
#     actual_vertices = polygon.vertices
#     assert expected_vertices == actual_vertices
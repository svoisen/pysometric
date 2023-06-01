from math import cos, sin

import numpy as np

from .vector import Vector3


def x_axis_rot_mat(angle: float) -> np.array:
    cosr = cos(angle)
    sinr = sin(angle)
    return [[1, 0, 0], [0, cosr, -sinr], [0, sinr, cosr]]


def y_axis_rot_mat(angle: float) -> np.array:
    cosr = cos(angle)
    sinr = sin(angle)
    return [[cosr, 0, sinr], [0, 1, 0], [-sinr, 0, cosr]]


def z_axis_rot_mat(angle: float) -> np.array:
    cosr = cos(angle)
    sinr = sin(angle)
    return [[cosr, -sinr, 0], [sinr, cosr, 0], [0, 0, 1]]


def rotate_x(point: Vector3, angle: float, center: Vector3 = (0, 0, 0)) -> Vector3:
    px, py, pz = point
    cx, cy, cz = center

    translated = (px - cx, py - cy, pz - cz)
    matrix = x_axis_rot_mat(angle)
    rx, ry, rz = tuple(np.dot(matrix, translated))

    return (rx + cx, ry + cy, rz + cz)


def rotate_y(point: Vector3, angle: float, center: Vector3 = (0, 0, 0)) -> Vector3:
    px, py, pz = point
    cx, cy, cz = center

    translated = (px - cx, py - cy, pz - cz)
    matrix = y_axis_rot_mat(angle)
    rx, ry, rz = tuple(np.dot(matrix, translated))

    return (rx + cx, ry + cy, rz + cz)


def rotate_z(point: Vector3, angle: float, center: Vector3 = (0, 0, 0)) -> Vector3:
    px, py, pz = point
    cx, cy, cz = center

    translated = (px - cx, py - cy, pz - cz)
    matrix = z_axis_rot_mat(angle)
    rx, ry, rz = tuple(np.dot(matrix, translated))

    return (rx + cx, ry + cy, rz + cz)

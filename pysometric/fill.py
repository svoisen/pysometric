from enum import Enum
from math import radians, tan

import numpy as np
from shapely import Geometry, LineString, MultiLineString, total_bounds

DEFAULT_HATCH_ANGLE = radians(45)


class HatchStyle(Enum):
    HATCH = (1,)
    CROSS_HATCH = 2


def line_fill(geometry: Geometry, pitch: float) -> MultiLineString:
    hatches = []
    minX, minY, maxX, maxY = total_bounds(geometry)
    for i in np.arange(minX + pitch, maxX, pitch):
        hatches.append(LineString([(i, minY), (i, maxY)]))

    return MultiLineString(hatches).intersection(geometry)


def hatch_fill(
    geometry: Geometry, pitch: float, style: HatchStyle, angle=DEFAULT_HATCH_ANGLE
) -> MultiLineString:
    angle = min(max(radians(1), angle), radians(89))
    hatches = []
    min_x, min_y, maxX, maxY = total_bounds(geometry)
    width = maxX - min_x
    height = maxY - min_y
    extent = max(width, height)

    if style == HatchStyle.HATCH or style == HatchStyle.CROSS_HATCH:
        for i in np.arange(min_x - extent, maxX, pitch):
            hatches.append(LineString([(i, maxY), (i + height / tan(angle), min_y)]))

    if style == HatchStyle.CROSS_HATCH:
        for i in np.arange(min_x, maxX + 2 * extent, pitch):
            hatches.append(LineString([(i, maxY), (i - height / tan(angle), min_y)]))

    return MultiLineString(hatches).intersection(geometry)

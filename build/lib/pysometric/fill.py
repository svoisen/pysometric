from math import radians, tan, pi

import numpy as np
from shapely import Geometry, LineString, MultiLineString, bounds

DEFAULT_HATCH_ANGLE = radians(45)

def hatch_fill(
    geometry: Geometry, pitch: float, angle=DEFAULT_HATCH_ANGLE
) -> MultiLineString:
    hatches = []
    min_x, min_y, max_x, max_y = bounds(geometry)
    height = max_y - min_y

    if angle % pi == 0:
        for i in np.arange(min_y, max_y, pitch):
            hatches.append(LineString([(min_x, i), (max_x, i)]))
    else:
        hatch_width = 0 if angle == radians(90) else abs(height / tan(angle))
        for i in np.arange(min_x - hatch_width, max_x + hatch_width, pitch):
            hatches.append(LineString([(i, max_y), (i + height / tan(angle), min_y)]))

    return MultiLineString(hatches).intersection(geometry)

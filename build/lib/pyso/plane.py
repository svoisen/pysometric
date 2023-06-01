from enum import Enum


class Plane(Enum):
    """
    Enumeration defining the viewing planes within which a shape can be oriented.
    """

    YZ = (1,)
    XZ = (2,)
    XY = 3

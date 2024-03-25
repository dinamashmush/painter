import enum


class LineStyle(enum.Enum):
    SOLID = '1'
    DASHED = '2'
    DOTS = '3'

class State(enum.Enum):
    PAINT = "1"
    SELECT = "2"
    # ERASE = "3"
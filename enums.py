import enum


class LineStyle(enum.Enum):
    SOLID = '1'
    DASHED = '2'
    DOTS = '3'

class State(enum.Enum):
    PAINT = "1"
    SELECT = "2"
    RECT = "3"
    OVAL = "4"
    TEXT = "5"
    POLYGON = "6"
    TRIANGLE = "7"
    
class Shape(enum.Enum):
    RECT = "1"
    OVAL = "2"
    TRIANGLE = "3"
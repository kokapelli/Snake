from typing import Tuple, Union, Dict
from enum import Enum

class Point(object):
    __slots__ = ('x', 'y')
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def copy(self) -> 'Point':
        x = self.x
        y = self.y
        return Point(x, y)

    def to_dict(self) -> Dict[str, int]:
        d = {}
        d['x'] = self.x
        d['y'] = self.y
        return d

    def to_int(self) -> int:
        return self.x, self.y

    def __eq__(self, other: Union['Point', Tuple[int, int]]) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            return other[0] == self.x and other[1] == self.y
        elif isinstance(other, Point) and self.x == other.x and self.y == other.y:
            return True
        return False

    def __add__(self, other: Union['Point', Tuple[int, int]]) -> 'Point':
        if isinstance(other, tuple) and len(other) == 2:
            diffX = self.x + other[0]
            diffY = self.y + other[1]
            
            return Point(diffX, diffY)
        elif isinstance(other, Point):
            diffX = self.x + other.x
            diffY = self.y + other.y

            return Point(diffX, diffY)
        return None

    def __sub__(self, other: Union['Point', Tuple[int, int]]) -> 'Point':
        if isinstance(other, tuple) and len(other) == 2:
            diffX = self.x - other[0]
            diffY = self.y - other[1]

            return Point(diffX, diffY)
        elif isinstance(other, Point):
            diffX = self.x - other.x
            diffY = self.y - other.y

            return Point(diffX, diffY)
        return None

    def __neg__(self) -> 'Point':
        return Point((self.x*-1), (self.y*-1))

    def __repr__(self) -> str:
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

# (-1, 0) Move Up 
# (1, 0) Move Down
# (0, -1) Move Left
# (0, 1) Move Right
class Trajectory(Enum):
    UP    = Point(-1, 0)
    DOWN  = Point(1, 0)
    LEFT  = Point(0, -1)
    RIGHT = Point(0, 1)
    UPLEFT = Point(-1, -1)
    UPRIGHT = Point(-1, 1)
    DOWNLEFT = Point(1, -1)
    DOWNRIGHT = Point(1, 1)

    # Ugly temporary solution


    def __neg__(self) -> 'Point':
        if   self == self.UP    : return self.DOWN
        elif self == self.DOWN  : return self.UP
        elif self == self.LEFT  : return self.RIGHT
        elif self == self.RIGHT : return self.LEFT

    def __repr__(self) -> list:
        print("HEre")
        

    # One hot encoding
    def OHE(self) -> list:
        if   self == self.UP    : return [1, 0 ,0 ,0]
        elif self == self.DOWN  : return [0, 1 ,0 ,0]
        elif self == self.LEFT  : return [0, 0 ,1 ,0]
        elif self == self.RIGHT : return [0, 0 ,0 ,1]
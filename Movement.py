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

    @classmethod
    def from_dict(cls, d: Dict[str, int]) -> 'Point':
        return Point(d['x'], d['y'])

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

    def __neg__(self) -> 'Point':
        return Point((self.x*-1), (self.y*-1))

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return '({}, {})'.format(self.x, self.y)


# (-1, 0) Move Up 
# (1, 0) Move Down
# (0, -1) Move Left
# (0, 1) Move Right
class Trajectory(Enum):
    UP    = Point(-1, 0)
    DOWN  = Point(1, 0)
    LEFT  = Point(0, -1)
    RIGHT = Point(0, 1)
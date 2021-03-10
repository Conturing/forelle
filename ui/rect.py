from dataclasses import dataclass
from typing import Tuple


@dataclass(init=True, eq=True, frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    def contains_point(self, item: Tuple[int, int]) -> bool:
        return self.x <= item[0] <= self.x + self.width and self.y <= item[1] <= self.y + self.height

    def contains_rect(self, item: Tuple[int, int, int, int]) -> bool:
        return self.x <= item[0] \
               and item[0] + item[2] <= self.x + self.width \
               and self.y <= item[1] \
               and item[1] + item[3] <= self.y + self.height

    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

    def __getitem__(self, item: int):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.width
        elif item == 3:
            return self.height
        else:
            raise ValueError(item)
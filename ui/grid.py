from typing import Optional, Sequence, Iterable, Iterator, Dict, Tuple, List, Union

import pygame
from pygame import Surface
from pygame_widgets.widget import WidgetBase

import itertools

from ui.text_render import TextRender
from ui.frame import Frame
from ui.rect import Rect

default_args = {
    'background_color': (250, 250, 250),
    'text_color': (10, 10, 10),
    'font_size': 20
}


def fill_stream(stream: Sequence[int], sum: int, num: int) -> List:
    result = list()
    for value in stream:
        sum -= value
        num -= 1
        result.append(value)

    result += [sum // max(num, 1)] * max(num, 0)
    return result


def cumsum(seq: Sequence[int]) -> List[int]:
    result = list()
    partial_sum = 0
    for value in seq:
        partial_sum += value
        result.append(partial_sum)
    return result


class Grid(WidgetBase):
    Data = Dict[Tuple[int, int], Surface]
    RectLike = Union[Rect, Tuple[int, int, int, int]]

    data: Data
    rows: int
    columns: int
    cell_width: List[int]
    cell_height: List[int]
    cell_width_c: List[int]
    cell_height_c: List[int]
    scroll_x: Optional[int]
    scroll_y: Optional[int]

    def __init__(self,
                 win: Surface, x: int, y: int, width: int, height: int, *,
                 columns: int, rows: int,
                 cell_width: Optional[Sequence[int]] = None,
                 cell_height: Optional[Sequence[int]] = None,
                 cell_data: Sequence[Data] = None,
                 scroll_x: Optional[int] = None,
                 scroll_y: Optional[int] = None):

        super().__init__(win, x, y, width, height)

        if cell_width is None:
            cell_width = list()
        if cell_height is None:
            cell_height = list()
        if cell_data is None:
            cell_data = dict()
        if scroll_x is None:
            scroll_x = 0
        if scroll_y is None:
            scroll_y = 0

        self.data = cell_data

        self.columns = columns
        self.rows = rows
        self.cell_width = fill_stream(cell_width, width, self.columns)
        self.cell_height = fill_stream(cell_height, height, self.rows)

        self.cell_height_c = cumsum([0] + self.cell_height)
        self.cell_width_c = cumsum([0] + self.cell_width)

        self.scroll_x = scroll_x
        self.scroll_y = scroll_y

    def set_data(self, data: Data):
        self.data = data

    def update_data(self, datum: Surface, row: int, column: int):
        self.data.__setitem__((row, column), datum)

    def cell_rect(self, row: int, column: int) -> RectLike:
        return Rect(self._x + self.cell_width_c[column],
                    self._y + self.cell_height_c[row],
                    self.cell_width[column],
                    self.cell_height[row])

    def outer_rect(self) -> RectLike:
        return Rect(self._x, self._y, self._width, self._height)

    def scroll(self, relative_x: int, relative_y: int):
        self.scroll_x += relative_x
        self.scroll_y += relative_y

    def data_interval(self):
        return Rect(self.scroll_x, self.scroll_y, self.columns, self.rows)

    def listen(self, events: Sequence[pygame.event.Event]):
        super().listen(events)

    def draw(self):
        for (row, column), surface in self.data.items():
            if self.data_interval().contains_point((column, row)):
                self.win.blit(surface, self.cell_rect(row - self.scroll_y, column - self.scroll_x).to_tuple())

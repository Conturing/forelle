from typing import Optional, Sequence, Iterable, Iterator, Dict, Tuple

import pygame
from pygame import Surface
from pygame_widgets.widget import WidgetBase

import itertools

from ui.grid import Grid
from ui.text_render import TextRender
from ui.frame import Frame

default_args = {
    'background_color': (250, 250, 250),
    'inner_padding': (2, 2, 2, 2),
    'text_color': (10, 10, 10),
    'font_size': 20
}


def fill_stream(stream: Sequence[int], sum: int, num: int) -> Sequence:
    result = list()
    for value in stream:
        sum -= value
        num -= 1
        result.append(value)

    result += [sum // max(num, 1)] * max(num, 0)
    return result


class Table(WidgetBase):

    highlights: Dict[Tuple[int, int], Tuple[int, int, int]]

    def __init__(self,
                 win: Surface, x: int, y: int, width: int, height: int, *,
                 columns: int, rows: int,
                 cell_width: Optional[Sequence[int]] = None,
                 cell_height: Optional[Sequence[int]] = None,
                 **kwargs):
        super().__init__(win, x, y, width, height)
        self.parameters = default_args.copy()
        self.parameters.update(**kwargs)

        self.data = kwargs.get('data', list(list()))

        self.background = Frame(win, x, y, width, height,
                                background_color=self.parameters.get('background_color'),
                                inner_padding=self.parameters.get('inner_padding'))
        self.text_font = TextRender(self.parameters.get('font_size'),
                                    text_color=self.parameters.get('text_color'))
        self.grid = Grid(self.win,
                         *self.background.inner_rect(),
                         columns=columns, rows=rows,
                         cell_width=cell_width, cell_height=cell_height)

        self.highlights = self.parameters.get('highlights', dict())

    def set_data(self, data: Sequence[Sequence[str]]):
        self.data = data

    def listen(self, events: Sequence[pygame.event.Event]):
        super().listen(events)
        self.background.listen(events)
        self.grid.listen(events)

    def draw(self):
        self.background.draw()

        for (row, column), color in self.highlights.items():
            pygame.draw.rect(self.win, color, self.grid.cell_rect(row, column).to_tuple())

        data = dict()
        for row, row_data in enumerate(self.data):
            for column, cell_datum in enumerate(row_data):
                surface = self.text_font.render(cell_datum)
                data.__setitem__((row, column), surface)

        self.grid.set_data(data)
        self.grid.draw()




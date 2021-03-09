from typing import Optional, Sequence, Iterable, Iterator, Dict, Tuple

import pygame
from pygame import Surface
from pygame_widgets.widget import WidgetBase

import itertools

default_args = {
    'background_color': (250, 250, 250),
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

    def __init__(self, win: Surface, x: int, y: int, width: int, height: int, columns: int, rows: int, **kwargs):
        super().__init__(win, x, y, width, height)
        self.parameters = default_args.copy()
        self.parameters.update(**kwargs)

        self.data = kwargs.get('data', list(list()))

        self.columns = columns
        self.rows = rows
        self.cell_width = fill_stream(kwargs.get('cell_width', list()), width, self.columns)
        self.cell_height = fill_stream(kwargs.get('cell_height', list()), height, self.rows)
        self.text_font = self.parameters.get('font', pygame.font.SysFont('calibri', self.parameters['font_size']))
        self.highlights: Dict[Tuple[int, int], Tuple[int, int, int]] = self.parameters.get('highlights', dict())

    def set_data(self, data: Sequence[Sequence[str]]):
        self.data = data

    def listen(self, events: Sequence[pygame.event.Event]):
        super().listen(events)

    def draw(self):
        pygame.draw.rect(self.win, self.parameters['background_color'], (self._x, self._y, self._width, self._height))

        x = self._x
        y = self._y
        row = 0
        column = 0

        for height, row_data in zip(self.cell_height, self.data):
            for width, cell_data in zip(self.cell_width, row_data):
                if (row, column) in self.highlights:
                    pygame.draw.rect(self.win, self.highlights[(row, column)], (x, y, width, height))

                text = self.text_font.render(cell_data, True, self.parameters['text_color'])
                self.win.blit(text, (x, y, width, height))

                x += width
                column += 1

            y += height
            row += 1
            x = self._x
            column = 0


from os import PathLike
from typing import Optional, Union, Tuple, List

import pygame
from pygame.color import Color
from pygame.font import Font
from pygame_widgets.widget import WidgetBase


class Frame(WidgetBase):

    Color = Union[
        Color, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
    ]
    Rect = Tuple[int, int, int, int]

    def __init__(self,
                 win: pygame.Surface, x: int, y: int, width: int, height: int, *,
                 background_color: Optional[Color] = None,
                 inner_padding: Optional[Rect] = None):
        super().__init__(win, x, y, width, height)

        if background_color is None:
            background_color = Color(250, 250, 250, 255)
        if inner_padding is None:
            inner_padding = (0, 0, 0, 0)

        self.background_color = background_color
        self.inner_padding = inner_padding

    def listen(self, events):
        super().listen(events)

    def draw(self):
        super().draw()
        pygame.draw.rect(self.win, self.background_color, self.outer_rect())

    def outer_rect(self) -> Rect:
        return (self._x, self._y, self._width, self._height)

    def inner_rect(self) -> Rect:
        return (self._x + self.inner_padding[0],
                self._y + self.inner_padding[1],
                self._width - self.inner_padding[0] - self.inner_padding[2],
                self._height - self.inner_padding[1] - self.inner_padding[3])

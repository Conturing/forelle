from os import PathLike
from typing import Optional, Union, Tuple, List

import pygame
from pygame.color import Color
from pygame.font import Font


class TextRender:

    Color = Union[
        Color, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
    ]
    Path = Union[
        str, PathLike
    ]

    def __init__(self,
                 font_size: Optional[int] = None,
                 sysfont_name: Optional[str] = None, *,
                 custom_font_path: Optional[Path] = None,
                 text_color: Optional[Color] = None,
                 background_color: Optional[Color] = None):

        if sysfont_name is None:
            sysfont_name = 'calibri'
        if font_size is None:
            font_size = 20
        if text_color is None:
            text_color = Color(10, 10, 10, 255)
        if custom_font_path is None:
            font = pygame.font.SysFont(sysfont_name, font_size)
        else:
            font = pygame.font.Font(custom_font_path, font_size)

        self.font_size = font_size
        self.font = font
        self.text_color = text_color
        self.background_color = background_color

    def render(self, text: str) -> pygame.Surface:
        return self.font.render(text, True, self.text_color, self.background_color)

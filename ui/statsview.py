from typing import Optional, List, Tuple, Sequence

from pygame import Surface, Color

from ui.pygame.frame import Frame
from ui.pygame.text_render import TextRender


class StatsView(Frame):

    stats: List[Tuple[str, Sequence[str]]]

    def __init__(self,
                 win: Surface,
                 x: int,
                 y: int,
                 width: int,
                 height: int, *,
                 font_size: Optional[int] = None,
                 background_color: Optional[TextRender.Color] = None):
        if background_color is None:
            background_color = Color(250, 250, 250, 255)

        super().__init__(win, x, y, width, height, background_color=background_color)

        self.text_font = TextRender(font_size=font_size)
        self.stats = list()

    def set_stats(self, stats: List[Tuple[str, Sequence[str]]]):
        self.stats = stats

    def listen(self, events):
        super().listen(events)

    def draw(self):
        super().draw()
        y = self._y
        for state in self.stats:
            surface = self.text_font.render(f'{state[0]} ... {", ".join(state[1][0:3])}')
            self.win.blit(surface, (self._x, y, self._width, self._height))
            y += self.text_font.font_size

from typing import List, Tuple

import pygame
from pygame_widgets.widget import WidgetBase

import chess
from chess.pgn import Game

default_args = {
    'background_color': (255, 255, 255),
    'text_color': (10, 10, 10),
    'text_padding': (4, 5, 0, 0),  # left up right bottom
    'number_offset': (0, 0),
    'font_size': 20
}


class GameView(WidgetBase):

    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, game: Game = None, **kwargs):
        super().__init__(screen, x, y, width, height)

        if game is None:
            game = Game()
        self.game = game
        self.current_game = self.game

        self.config = default_args.copy()
        self.config.update(**kwargs)

        self.text_font = self.config.get('font', pygame.font.SysFont('calibri', self.config['font_size']))

    def listen(self, events):
        super().listen(events)

    def draw(self):
        pygame.draw.rect(self.win, self.config['background_color'], (self._x, self._y, self._width, self._height))
        temp_board = chess.Board()
        for ply, node in enumerate(self.game.mainline()):
            if ply % 2 == 0:
                text = self.text_font.render(f'{ply // 2 + 1}. ', True, self.config['text_color'])
                self.win.blit(text, (self._x + 4, self._y + 5 + 20 * (ply // 2)))
            san = temp_board.san(node.move)
            temp_board.push(node.move)
            text = self.text_font.render(san, True, self.config['text_color'])
            self.win.blit(text, (self._x + 35 + (self._width // 2) * (ply % 2), self._y + 5 + 20 * (ply // 2)))

    def game_state(self) -> Game:
        return self.game

    def apply_moves(self, moves: List[Tuple[chess.Move, str]]):
        for move, comment in moves:
            self.current_game = self.current_game.add_variation(move, comment=comment)

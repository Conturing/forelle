from array import array
import random
from typing import Dict, Any, Optional, Tuple

import pygame
from pygame import Surface
import chess
from pygame_widgets.widget import WidgetBase

from pieces import PieceRenderer

default_theme = {
    'white_tile': (239, 217, 181),
    'black_tile': (181, 137, 99)
}


class ChessBoardView(WidgetBase):

    def __init__(self,
                 screen: Surface, x: int, y: int, width: int, height: int, *,
                 initial_position: Optional[chess.Board] = None,
                 squares: Optional[Tuple[int, int]] = None,
                 piece_render: Optional[PieceRenderer] = None):
        super().__init__(screen, x, y, width, height)

        if initial_position is None:
            initial_position = chess.Board()
        if squares is None:
            squares = (8, 8)
        if piece_render is None:
            piece_render = PieceRenderer()

        self.tile_size = (width // squares[0], height // squares[1])
        self.theme = default_theme.copy()
        self.board = initial_position
        self.piece_render = piece_render

    def draw(self):
        super().draw()
        self.draw_board()
        self.draw_pieces(self.piece_render)

    def listen(self, events):
        super().listen(events)

    def draw_board(self):
        for sq in chess.SQUARES:
            tile = self.theme['white_tile'] if (sq + sq // 8) % 2 == 0 else self.theme['black_tile']
            pygame.draw.rect(self.win, tile, self._translate_rect_inv(sq))

    def draw_pieces(self, pr: PieceRenderer):
        for sq in chess.SQUARES:
            if self.board.piece_at(sq) is not None:
                pr.render(self.board.piece_at(sq), self.win, self._translate_rect_inv(sq))

    def _translate_inv(self, square: chess.Square) -> Tuple[int, int]:
        return (self._x + chess.square_file(square) * self.tile_size[0],
                self._y + (7 - chess.square_rank(square)) * self.tile_size[1])

    def _translate_rect_inv(self, square: chess.Square) -> Tuple[int, int, int, int]:
        return (self._x + chess.square_file(square) * self.tile_size[0],
                self._y + (7 - chess.square_rank(square)) * self.tile_size[1],
                self.tile_size[0],
                self.tile_size[1])

    def _translate(self, position: Tuple[int, int]) -> Optional[chess.Square]:
        square = (position[0] - self._x) // self.tile_size[0] \
               + (7 - (position[1] - self._y) // self.tile_size[1]) * 8
        if square in chess.SQUARES:
            return square
        return None

    def game_state(self) -> chess.Board:
        return self.board

    def display(self, board):
        self.board = board

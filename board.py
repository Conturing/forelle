from array import array
import random
from typing import Dict, Any, Optional, Tuple

import pygame
import chess

from pieces import PieceRenderer

default_args = {
    'tile_size': (100, 100),
    'chessboard_begin': (100, 100),
    'white_tile': (239, 217, 181),
    'black_tile': (181, 137, 99)
}


class ChessBoard:

    def __init__(self, screen: pygame.Surface, config: Optional[Dict] = None, board: Optional[chess.Board] = None):
        if config is None:
            config = dict()
        if board is None:
            board = chess.Board()
        self.screen = screen
        self.config = default_args.copy()
        self.config.update(config)
        self.board = board

    def draw_board(self):
        for sq in chess.SQUARES:
            tile = self.config['white_tile'] if (sq + sq // 8) % 2 == 0 else self.config['black_tile']
            pygame.draw.rect(self.screen, tile, self.translate_rect_inv(sq))

    def draw_pieces(self, pr: PieceRenderer):
        for sq in chess.SQUARES:
            if self.board.piece_at(sq) is not None:
                pr.render(self.board.piece_at(sq), self.screen, self.translate_rect_inv(sq))

    def translate_inv(self, square: chess.Square) -> Tuple[int, int]:
        return (self.config['chessboard_begin'][0] + chess.square_file(square) * self.config['tile_size'][0],
                self.config['chessboard_begin'][1] + (7 - chess.square_rank(square)) * self.config['tile_size'][1])

    def translate_rect_inv(self, square: chess.Square) -> Tuple[int, int, int, int]:
        return (self.config['chessboard_begin'][0] + chess.square_file(square) * self.config['tile_size'][0],
                self.config['chessboard_begin'][1] + (7 - chess.square_rank(square)) * self.config['tile_size'][1],
                self.config['tile_size'][0],
                self.config['tile_size'][1])

    def translate(self, position: Tuple[int, int]) -> Optional[chess.Square]:
        square = (position[0] - self.config['chessboard_begin'][0]) // self.config['tile_size'][0] \
               + (7 - (position[1] - self.config['chessboard_begin'][1]) // self.config['tile_size'][1]) * 8
        if square in chess.SQUARES:
            return square
        return None

    def parameter(self, key: str) -> Optional[Any]:
        return self.config.get(key)

    def game_state(self) -> chess.Board:
        return self.board

    def set_board(self, board):
        self.board = board

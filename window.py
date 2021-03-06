from array import array
import random
from typing import Dict, Any, Optional, Tuple

import pygame
import chess

from board import ChessBoard
from pieces import PieceRenderer

default_args = {
    'window': (1000, 1000),
    'chessboard_begin': (100, 100),
    'background_color': (50, 50, 50)
}


class Window:

    def __init__(self, config: Dict = None):
        if config is None:
            config = dict()

        self.config = default_args.copy()
        self.config.update(config)

        pygame.init()

        self.screen = pygame.display.set_mode(self.config['window'])
        pygame.display.set_caption('Forelle')

        self.text_font = pygame.font.SysFont('calibri', 28)
        self.screen.fill(self.config['background_color'])

        self.pr = PieceRenderer()
        self.clock = pygame.time.Clock()

        self.board = ChessBoard(self.screen, self.config)

    def main_loop(self):
        loop = True
        selected_square = None
        redraw = True
        chessboard = self.board.game_state()
        while loop:
            for event in pygame.event.get():

                legal_moves = list(chessboard.legal_moves)

                if self.board.game_state().turn == chess.BLACK and len(legal_moves) > 0:
                    move = random.sample(legal_moves, 1)[0]
                    chessboard.push(move)
                    redraw = True

                if event.type == pygame.QUIT:
                    loop = False
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    loop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    square = self.board.translate(pygame.mouse.get_pos())
                    redraw = True
                    if square in chess.SQUARES:
                        if selected_square is None:
                            legal_moves = list(filter(lambda x: x.to_square == square, chessboard.legal_moves))
                            if len(legal_moves) == 1:
                                chessboard.push(legal_moves[0])
                                selected_square = None
                            else:
                                selected_square = square
                        elif selected_square == square:
                            selected_square = None
                        else:
                            legal_moves = list(filter(lambda x: x.from_square == selected_square and x.to_square == square, chessboard.legal_moves))
                            if len(legal_moves) > 0:
                                chessboard.push(legal_moves[0])
                            else:
                                selected_square = square
                    else:
                        selected_square = None

                if redraw:
                    redraw = False
                    self.board.draw_board()
                    self.board.draw_pieces(self.pr)
                    if selected_square is not None:
                        for move in filter(lambda x: x.from_square == selected_square, chessboard.legal_moves):
                            rect = self.board.translate_rect_inv(move.to_square)
                            pygame.draw.circle(self.screen,
                                               (0,0,0),
                                               (rect[0] + rect[2]//2, rect[1] + rect[3]//2),
                                               5)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

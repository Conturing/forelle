from array import array
import random
from time import sleep
from typing import Dict, Any, Optional, Tuple

import pygame
import chess
from chess.pgn import Game
from chess.engine import SimpleEngine

from board import ChessBoard
from game import GameView
from pieces import PieceRenderer

import datetime as dt

default_args = {
    'window': (1400, 1000),
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

        self.text_font = pygame.font.SysFont('calibri', 20)
        self.screen.fill(self.config['background_color'])

        self.piece_renderer = PieceRenderer()
        self.clock = pygame.time.Clock()

        self.game = Game()
        self.board = ChessBoard(self.screen, self.config)

        self._game = GameView(self.screen, 980, 100, 200, 800)

    def main_loop(self):
        loop = True
        selected_square = None
        redraw = True
        chessboard = self.board.game_state()
        moves = list()
        saved = False

        self._game.game_state().headers['White'] = 'player'
        self._game.game_state().headers['Black'] = 'random'

        self._game.register_on_change(lambda game: self.board.set_board(game.board()))

        while loop:

            legal_moves = list(chessboard.legal_moves)

            #if self.board.game_state().turn == chess.BLACK and len(legal_moves) > 0 and not saved:
                #moves.append(random.sample(legal_moves, 1)[0])
                #redraw = True

            for move in moves:
                self._game.apply_moves([(move, '')])
                chessboard.push(move)

            moves.clear()

            if (chessboard.is_checkmate() or chessboard.is_stalemate() or chessboard.is_insufficient_material()) and not saved:
                saved = True
                print(f'final position after {chessboard.ply()} plies, saving ...')
                print(self._game.game_state(), file=open(f'games/player vs random ({chessboard.ply()}) '
                                                         f'- {dt.datetime.now():%Y-%m-%dT%H-%M-%S}.pgn', 'w'),
                      end='\n\n')

            events = pygame.event.get()
            self._game.listen(events)

            for event in events:
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
                                moves.append(legal_moves[0])
                                selected_square = None
                            else:
                                selected_square = square
                        elif selected_square == square:
                            selected_square = None
                        else:
                            legal_moves = list(
                                filter(lambda x: x.from_square == selected_square and x.to_square == square,
                                       chessboard.legal_moves))
                            if len(legal_moves) > 0:
                                moves.append(legal_moves[0])
                            else:
                                selected_square = square
                    else:
                        selected_square = None

            self.board.draw_board()
            self.board.draw_pieces(self.piece_renderer)

            self._game.draw()

            if selected_square is not None:
                for move in filter(lambda x: x.from_square == selected_square, chessboard.legal_moves):
                    rect = self.board.translate_rect_inv(move.to_square)
                    pygame.draw.circle(self.screen,
                                       (0, 0, 0),
                                       (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2),
                                       5)
            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()

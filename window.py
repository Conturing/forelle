from typing import Dict, List

import pygame
import chess
from chess.engine import SimpleEngine

from ui.board import ChessBoardView
from game import GameControl
from pieces import PieceRenderer

import datetime as dt

from ui.statsview import StatsView

default_theme = {
    'window': (1400, 1000),
    'chessboard_begin': (100, 100),
    'background_color': (50, 50, 50)
}

stockfish_path = ''

class Window:

    def __init__(self, config: Dict = None):
        if config is None:
            config = dict()

        self.theme = default_theme.copy()
        self.theme.update(config)

        pygame.init()

        self.screen = pygame.display.set_mode(self.theme['window'])
        pygame.display.set_caption('Forelle')

        self.text_font = pygame.font.SysFont('calibri', 20)
        self.screen.fill(self.theme['background_color'])

        self.piece_renderer = PieceRenderer()
        self.clock = pygame.time.Clock()

        self.board = ChessBoardView(self.screen, 100, 100, 800, 800, piece_render=self.piece_renderer)
        self.game = GameControl(self.screen, 980, 170, 300, 800)
        self.stats = StatsView(self.screen, 980, 100, 300, 60)

    def main_loop(self):
        loop = True
        selected_square = None
        redraw = True
        chessboard = self.board.game_state()
        moves = list()
        saved = False

        self.game.game_state().game().headers['White'] = 'player'
        self.game.game_state().game().headers['Black'] = 'random'

        self.game.register_on_change(lambda game: self.board.display(game.board()))

        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

        while loop:

            legal_moves = list(chessboard.legal_moves)

            #if self.board.game_state().turn == chess.BLACK and len(legal_moves) > 0 and not saved:
                #moves.append(random.sample(legal_moves, 1)[0])
                #redraw = True

            def line(board: chess.Board, moves: List[chess.Move]) -> List[str]:
                result = list()
                for move in moves:
                    result.append(board.san(move))
                    board.push(move)
                for _ in moves:
                    board.pop()
                return result

            for move in moves:
                self.game.apply_moves([(move, '')])
                chessboard.push(move)
                info_multipv = engine.analyse(self.game.game_state().board(), chess.engine.Limit(time=0.2), multipv=3)
                stats = [(info['score'].pov(chess.WHITE), line(chessboard, info.get('pv', list()))) for info in info_multipv]
                self.stats.set_stats(stats)

            moves.clear()

            if (chessboard.is_checkmate() or chessboard.is_stalemate() or chessboard.is_insufficient_material()) and not saved:
                saved = True
                print(f'final position after {chessboard.ply()} plies, saving ...')
                print(self.game.game_state(), file=open(f'games/player vs random ({chessboard.ply()}) '
                                                         f'- {dt.datetime.now():%Y-%m-%dT%H-%M-%S}.pgn', 'w'),
                      end='\n\n')

            events = pygame.event.get()
            self.game.listen(events)
            self.board.listen(events)
            self.stats.listen(events)

            for event in events:
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    loop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    square = self.board._translate(pygame.mouse.get_pos())
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

            self.board.draw()
            self.board.draw_pieces(self.piece_renderer)

            self.game.draw()
            self.stats.draw()
            if selected_square is not None:
                for move in filter(lambda x: x.from_square == selected_square, chessboard.legal_moves):
                    rect = self.board._translate_rect_inv(move.to_square)
                    pygame.draw.circle(self.screen,
                                       (0, 0, 0),
                                       (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2),
                                       5)
            pygame.display.update()

            self.clock.tick(60)

        engine.quit()
        pygame.quit()

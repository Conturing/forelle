from typing import List, Tuple, Sequence, Callable, Any, Optional

import pygame
from pygame_widgets.widget import WidgetBase

import chess
from chess.pgn import Game, GameNode

from table import Table

default_args = {
    'background_color': (255, 255, 255),
    'text_color': (10, 10, 10),
    'text_padding': (4, 5, 0, 0),  # left up right bottom
    'number_offset': (0, 0),
    'font_size': 20,
    'highlight_color': (100, 100, 255, 150)
}


class GameView(Table):

    game: Game
    current_game: GameNode
    OnChangeHandle = Callable[[GameNode], None]
    on_change_handlers: List[OnChangeHandle]

    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, game: Optional[Game] = None, **kwargs):
        super().__init__(screen, x, y, width, height, 3, height // 20, cell_width=[35], **kwargs)

        if game is None:
            game = Game()
        self.game = game
        self.current_game = self.game

        self.on_change_handlers = list()

        self.config = default_args.copy()
        self.config.update(**kwargs)

    def listen(self, events: Sequence[pygame.event.Event]):
        super().listen(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if len(self.current_game.variations) > 0:
                    self._update_current_game(self.current_game.variations[0])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self._update_current_game(self.current_game.parent)

    def register_on_change(self, f: OnChangeHandle):
        self.on_change_handlers.append(f)

    def _update_current_game(self, to: GameNode):
        self.current_game = to
        for handler in self.on_change_handlers:
            handler(self.current_game)

    def draw(self):
        data = list()
        column_data = list()
        temp_board = chess.Board()

        for ply, node in enumerate(self.game.mainline()):
            if ply % 2 == 0:
                if len(column_data) > 0:
                    data.append(column_data)
                column_data = list()
                column_data.append(f'{ply // 2 + 1}. ')
            san = temp_board.san(node.move)
            temp_board.push(node.move)
            column_data.append(san)
            if node == self.current_game:
                self.highlights = {(ply // 2, ply % 2 + 1): self.config['highlight_color']}

        if len(column_data) > 0:
            data.append(column_data)

        self.set_data(data)
        super().draw()

    def game_state(self) -> GameNode:
        return self.current_game

    def apply_moves(self, moves: List[Tuple[chess.Move, str]]):
        for move, comment in moves:
            self._update_current_game(self.current_game.add_variation(move, comment=comment))

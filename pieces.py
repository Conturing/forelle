from typing import Tuple

import chess
import pygame


class PieceRenderer:

    def __init__(self, theme: str = 'kosal'):
        self.theme = {}
        for piece in chess.PIECE_TYPES:
            self.theme[piece] = pygame.image.load(f'pieces/{theme}/black_{chess.piece_name(piece)}.png')
            self.theme[piece+6] = pygame.image.load(f'pieces/{theme}/white_{chess.piece_name(piece)}.png')

    def render(self, piece: chess.Piece, screen: pygame.Surface, box: Tuple[int, int, int, int]):
        image = self.theme.get(piece.piece_type + 6*piece.color)
        screen.blit(image, box)

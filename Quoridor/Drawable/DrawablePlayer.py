import pygame

import Player


class DrawablePlayer(Player.Player):
    def __init__(self, n, board, sp_handler, color, n_players):
        super().__init__(n, board, sp_handler, n_players)
        self.c = color

    def draw(self, board, surface):
        square_w, square_h = board.square_dimension()
        x, y = board.get_absolute_pos((self.x, self.y), self.n)
        x, y = board.get_position_on_board(x, y, square_w, square_h)
        pygame.draw.ellipse(surface, self.c, (x, y, square_w, square_h))

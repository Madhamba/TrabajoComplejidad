import pygame

import Board


class DrawableBoard(Board.Board):
    def __init__(self, n, m, x, y, width, height, separation, color):
        super().__init__(n, m)
        self.x, self.y = x, y
        self.w, self.h = width, height
        self.c = color
        self.s = separation

    def draw_edge(self, edge, surface):
        square_w, square_h = self.square_dimension()
        u_x, u_y = self.get_position_on_board(edge[0][0], edge[0][1], square_w, square_h)
        v_x, v_y = self.get_position_on_board(edge[1][0], edge[1][1], square_w, square_h)

        if u_x == v_x:  # equal x
            x = u_x
            y = max(u_y, v_y) - self.s
            pygame.draw.rect(surface, self.c, (x, y, square_w, self.s))
        else:
            x = max(u_x, v_x) - self.s
            y = u_y
            pygame.draw.rect(surface, self.c, (x, y, self.s, square_h))

    def draw_barrier(self, barrier, surface):
        edge1, edge2 = barrier
        self.draw_edge(edge1, surface)
        self.draw_edge(edge2, surface)

    def draw_barriers(self, surface):
        for barrier in self.barriers:
            self.draw_barrier(barrier, surface)

    def square_dimension(self):
        square_w = self.w // self.n - self.s
        square_h = self.h // self.m - self.s
        return square_w, square_h

    def get_position_on_board(self, x, y, square_w, square_h):
        x = self.x + x * square_w + x * self.s
        y = self.y + y * square_h + y * self.s
        return x, y

    def draw(self, surface):
        square_w, square_h = self.square_dimension()
        for y in range(self.m):
            for x in range(self.n):
                square_x, square_y = self.get_position_on_board(x, y, square_w, square_h)
                pygame.draw.rect(surface, self.c, (square_x, square_y, square_w, square_h), 2)

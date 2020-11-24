import Abstract.Subject

import Util.util


class Board(Abstract.Subject.Subject):
    def __init__(self, n, m):
        super().__init__()
        self.n = n
        self.m = m
        self.barriers = []

    def set_barrier(self, edge1, edge2, n):
        u1_x, u1_y = self.get_absolute_pos((edge1[0][0], edge1[0][1]), n)
        v1_x, v1_y = self.get_absolute_pos((edge1[1][0], edge1[1][1]), n)

        u2_x, u2_y = self.get_absolute_pos((edge2[0][0], edge2[0][1]), n)
        v2_x, v2_y = self.get_absolute_pos((edge2[1][0], edge2[1][1]), n)
        barrier = (((u1_x, u1_y), (v1_x, v1_y)), ((u2_x, u2_y), (v2_x, v2_y)))

        self.barriers.append(barrier)

    def remove_barrier(self, edge1, edge2, n):
        u1_x, u1_y = self.get_absolute_pos((edge1[0][0], edge1[0][1]), n)
        v1_x, v1_y = self.get_absolute_pos((edge1[1][0], edge1[1][1]), n)

        u2_x, u2_y = self.get_absolute_pos((edge2[0][0], edge2[0][1]), n)
        v2_x, v2_y = self.get_absolute_pos((edge2[1][0], edge2[1][1]), n)
        barrier = (((u1_x, u1_y), (v1_x, v1_y)), ((u2_x, u2_y), (v2_x, v2_y)))

        self.barriers.remove(barrier)

    def get_absolute_pos(self, relative_pos, n_player):
        rotations = n_player
        board_center = self.m // 2, self.n // 2
        x, y = Util.util.rotate(relative_pos[0], relative_pos[1], 90 * -rotations, board_center)
        return x, y

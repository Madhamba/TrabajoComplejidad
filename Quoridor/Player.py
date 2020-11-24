import Abstract.Observer
import Abstract.Movable

import Action.impl.MoveAction
import Action.impl.BarrierAction

import Util.util

import PlayerBoard


class Player(Abstract.Observer.Observer, Abstract.Movable.Movable):
    def __init__(self, n, board, sp_handler, n_players):
        self.n = n
        self.x, self.y = board.n // 2, board.m - 1
        self.sp_handler = sp_handler
        self.board = PlayerBoard.PlayerBoard(board, n_players)
        board.attach(self)

    def is_in_winning_position(self):
        winning_nodes = [n for n, d in self.board.G.nodes(data=True) if d['is_winning_pos']]
        return (self.y, self.x) in winning_nodes

    def decide(self, board, opponent):
        shortest_path = self.sp_handler.get_shortest_path(self)
        o_shortest_path = opponent.sp_handler.get_shortest_path(opponent)

        if len(o_shortest_path) < len(shortest_path):
            board_center = board.m // 2, board.n // 2

            o_x, o_y = board.get_absolute_pos((opponent.x, opponent.y), opponent.n)
            o_x, o_y = Util.util.rotate(o_x, o_y, 90 * self.n, board_center)

            barrier_exists, edge1, edge2 = self.decide_barrier_position(opponent, o_x, o_y)

            if barrier_exists:
                board.set_barrier(edge1, edge2, self.n)
                board.notify(Action.impl.BarrierAction.BarrierAction(self, edge1, edge2))
                return

        last_pos = self.x, self.y
        self.y, self.x = shortest_path[1]
        new_pos = self.x, self.y
        board.notify(Action.impl.MoveAction.MoveAction(self, last_pos, new_pos))

    def decide_barrier_position(self, opponent, o_x, o_y):
        _edge1 = (opponent.y - 1, opponent.x - 0), (opponent.y - 0, opponent.x - 0)
        _edge2 = (opponent.y - 1, opponent.x - 1), (opponent.y - 0, opponent.x - 1)

        opponent.board.remove_edge(_edge1, _edge2)
        if len(opponent.sp_handler.get_shortest_path(opponent)) == 0:
            opponent.board.add_edge(_edge1, _edge2)
            return False, None, None

        opponent.board.add_edge(_edge1, _edge2)
        edge1 = (o_x + 0, o_y + 1), (o_x + 0, o_y + 0)
        edge2 = (o_x + 1, o_y + 1), (o_x + 1, o_y + 0)

        return True, edge1, edge2

    def update(self, subject, action):
        board_center = subject.m // 2, subject.n // 2

        if isinstance(action, Action.impl.MoveAction.MoveAction):
            if self == action.caller:
                return

            last_pos = subject.get_absolute_pos(action.last_pos, action.caller.n)
            last_pos = Util.util.rotate(last_pos[0], last_pos[1], 90 * self.n, board_center)

            new_pos = subject.get_absolute_pos(action.new_pos, action.caller.n)
            new_pos = Util.util.rotate(new_pos[0], new_pos[1], 90 * self.n, board_center)

            # TODO: fix methods for removing/adding node
            # self.board.add_node(last_pos[0], last_pos[1])
            # self.board.remove_node(new_pos[0], new_pos[1])
        else:
            edge1, edge2 = action.edge1, action.edge2

            u1_x, u1_y, v1_x, v1_y = self.get_edge_position(subject, action.caller.n, edge1, board_center)
            u2_x, u2_y, v2_x, v2_y = self.get_edge_position(subject, action.caller.n, edge2, board_center)

            self.board.remove_edge(((u1_y, u1_x), (v1_y, v1_x)), ((u2_y, u2_x), (v2_y, v2_x)))
            # if len(self.sp_handler.get_shortest_path(self)) < 1:
            #     print('her')
            #     self.board.add_edge(((u1_y, u1_x), (v1_y, v1_x)), ((u2_y, u2_x), (v2_y, v2_x)))
            #     subject.remove_barrier(edge1, edge2, action.caller.n)

    def get_positions(self, board, n, x, y, board_center):
        x, y = board.get_absolute_pos((x, y), n)
        return Util.util.rotate(x, y, 90 * self.n, board_center)

    def get_edge_position(self, board, n, edge, board_center):
        u_x, u_y = self.get_positions(board, n, edge[0][0], edge[0][1], board_center)
        v_x, v_y = self.get_positions(board, n, edge[1][0], edge[1][1], board_center)
        return u_x, u_y, v_x, v_y

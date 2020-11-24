import networkx as nx

from Util.networkx_util import *


class PlayerBoard:
    def __init__(self, board, n_players):
        self.G = nx.grid_2d_graph(board.n, board.m)

        nx.set_node_attributes(self.G, False, 'is_winning_pos')
        for i in range(board.n):
            self.G.nodes[(0, i)]['is_winning_pos'] = True

        self.remove_node(board.n // 2, 0)
        if n_players == 4:
            self.remove_node(0, board.m // 2)
            self.remove_node(board.n - 1, board.m // 2)

    def add_node(self, x, y):
        add_node_util(self.G, (y, x))

        add_edge_util(self.G, (y, x), (y, x - 1))
        add_edge_util(self.G, (y, x), (y, x + 1))

        if (y + 1, x) in self.G.nodes and (y - 1, x) in self.G.nodes:
            remove_edge_util(self.G, (y - 1, x), (y + 1, x))
            add_edge_util(self.G, (y, x), (y + 1, x))
            add_edge_util(self.G, (y, x), (y - 1, x))
        elif (y + 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y, x), (y - 1, x))
            remove_edge_util(self.G, (y + 2, x), (y + 1, x - 1))
            remove_edge_util(self.G, (y + 2, x), (y + 1, x + 1))
            add_edge_util(self.G, (y, x), (y + 2, x))
        elif (y - 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y, x), (y + 1, x))
            remove_edge_util(self.G, (y + 1, x), (y, x - 1))
            remove_edge_util(self.G, (y + 1, x), (y, x + 1))
            add_edge_util(self.G, (y, x), (y - 2, x))

        if get_attr_val(self.G, (y, x + 1), 'is_winning_pos') or get_attr_val(self.G, (y, x - 1), 'is_winning_pos'):
            self.G.nodes[(y, x)]['is_winning_pos'] = True
        else:
            self.G.nodes[(y, x)]['is_winning_pos'] = False

    def remove_node(self, x, y):
        remove_node_util(self.G, (y, x))

        if (y - 1, x) in self.G.nodes and (y + 1, x) in self.G.nodes:
            add_edge_util(self.G, (y + 1, x), (y - 1, x))
        elif (y + 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y + 2, x), (y + 1, x - 1))
            add_edge_util(self.G, (y + 2, x), (y + 1, x + 1))
        elif (y - 1, x) not in self.G.nodes:
            add_edge_util(self.G, (y + 1, x), (y, x - 1))
            add_edge_util(self.G, (y + 1, x), (y, x + 1))

    def remove_edge(self, edge1, edge2):
        remove_edge_util(self.G, edge1[0], edge1[1])
        remove_edge_util(self.G, edge2[0], edge2[1])

    def add_edge(self, edge1, edge2):
        add_edge_util(self.G, edge1[0], edge1[1])
        add_edge_util(self.G, edge2[0], edge2[1])


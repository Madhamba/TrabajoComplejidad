import pygame
import networkx as nx


def generate_player_information(player_number, board):
    graph = board.graph_representation.copy()
    m = board.m
    n = board.n

    info = {
        1: {'position': (0, m // 2), 'algorithm': nx.dijkstra_path, 'x_start': 0, 'y_start': n - 1, 'x_end': m - 1,
            'y_end': n - 1},
        2: {'position': (n - 1, m // 2), 'algorithm': nx.astar_path, 'x_start': 0, 'y_start': 0, 'x_end': m - 1,
            'y_end': 0},
        3: {'position': (n // 2, 0), 'algorithm': nx.shortest_path, 'x_start': m - 1, 'y_start': 0, 'x_end': m - 1,
            'y_end': n - 1},
        4: {'position': (n // 2, m - 1), 'algorithm': nx.dijkstra_path, 'x_start': 0, 'y_start': 0, 'x_end': 0,
            'y_end': n - 1}
    }

    player_info = info[player_number]
    position = player_info['position']
    algorithm = player_info['algorithm']

    x = board.square_width * position[1] + board.square_separation * position[1] + board.x
    y = board.square_height * position[0] + board.square_separation * position[0] + board.y

    if player_info['x_start'] == player_info['x_end']:
        for i in range(player_info['y_start'], player_info['y_end'] + 1):
            graph.nodes[(i, player_info['x_start'])]['is_winning_pos'] = True
    else:
        for i in range(player_info['x_start'], player_info['x_end'] + 1):
            graph.nodes[(player_info['y_start'], i)]['is_winning_pos'] = True

    return position, x, y, graph, algorithm


class Player:
    def __init__(self, player_number, board, color):  # r, color, board):
        # The player will be represented as a circle
        # Pos at this moment is the (x, y) coordinate of the center of that circle (the player)

        # As each cell of the board will be represented with a index, and that index is the top-left corner of the
        # square, it is convenient to change the pos coordinate from the center of the circle to the top-left corner
        # that surrounds it

        # To do that we add the value of the radios to each component of the pos coordinate resulting in the
        # following line
        # x, y = pos[0] + r, pos[1] + r

        # self.pos = (x, y)
        # self.r = r
        self.color = color
        self.width = board.square_width
        self.height = board.square_height
        self.position, self.x, self.y, self.graph_rep, self.algorithm = generate_player_information(player_number, board)

    # The draw method takes the screen where the player will be drawn and draws it.
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_in_winning_pos(self):
        if self.position in nx.get_node_attributes(self.graph_rep, 'is_winning_pos'):
            return True
        return False

    def get_next_best_move(self, board):
        position = self.position
        graph = self.graph_rep
        winning_pos = nx.get_node_attributes(graph, 'is_winning_pos')
        min_length = None
        shortest = None
        for node in winning_pos:
            shortest_path = self.algorithm(graph, source=position, target=node)
            if min_length is None or len(shortest_path) < min_length:
                min_length = len(shortest_path)
                shortest = shortest_path

        self.position = shortest[1]
        x = board.square_width * shortest[0][1] + board.square_separation * shortest[0][1] + board.x
        y = board.square_height * shortest[0][0] + board.square_separation * shortest[0][0] + board.y
        return x, y

import networkx as nx

from Square import Square


class Board:
    def __init__(self, pos, width, height, n, m, color):
        # n: rows, m: columns

        self.graph_representation = nx.grid_2d_graph(n, m)
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.n = n
        self.m = m

        # From the parameters that user send, we obtain the square height and width dimensions of each cell of
        # the board. In addition to that, we add a separation between each square that will represent the places
        # where users can block their opponents in the future

        # TODO: square_separation affects to the left and bottom squares too
        self.square_separation = 10
        self.square_height = int(height / n - self.square_separation)
        self.square_width = int(width / m - self.square_separation)

        # Fill a 2D array of squares with their width and height
        self.squares = []
        for i in range(n):
            for j in range(m):
                x = self.square_width * j + self.square_separation * j + self.x
                y = self.square_height * i + self.square_separation * i + self.y
                s = Square((x, y), self.square_width, self.square_height, color)
                self.squares.append(s)

    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)

import pygame

from Board import Board
from Player import Player


class Game:
    def __init__(self, screen_size, n, m, n_players):
        board_x, board_y = 10, 10
        board_width = screen_size[0] - 2 * board_x
        board_height = screen_size[1] - 2 * board_y

        self.board_color = (0, 0, 0)  # black
        self.background_color = (255, 255, 255)  # white

        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Algorithmic Complexity task: quoridor")
        self.board = Board((board_x, board_y), board_width, board_height, n, m, self.board_color)
        self.players = []
        for i in range(n_players):
            p = Player(i + 1, self.board, (0, 0, 0))
            self.players.append(p)

    def start(self):
        finished = False

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

            self.screen.fill(self.background_color)

            self.board.draw(self.screen)
            for player in self.players:
                player.draw(self.screen)

            pygame.display.flip()
            pygame.time.delay(100)

            for player in self.players:
                player.x, player.y = player.get_next_best_move(self.board)
                if player.is_in_winning_pos():
                    finished = True

        pygame.quit()

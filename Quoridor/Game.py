import pygame

import Drawable.DrawableBoard
import Drawable.DrawablePlayer

from random import choice

from ShortestPath.impl.AStarHandler import AStarHandler
from ShortestPath.impl.BellmanFordHandler import BellmanFordHandler
from ShortestPath.impl.DijkstraHandler import DijkstraHandler
from ShortestPath.impl.FloydWarshallHandler import FloydWarshallHandler

import Util.util


class Game:
    def __init__(self, m, n, n_players, screen_size):
        self.m, self.n = m, n
        self.n_players = n_players
        self.screen_size = screen_size
        self.board = Drawable.DrawableBoard.DrawableBoard(self.m, self.n,
                                                          10, 10,
                                                          screen_size[0] - 10, screen_size[1] - 10,
                                                          15, (0, 0, 0))

        self.players = {
            0: Drawable.DrawablePlayer.DrawablePlayer(0, self.board, AStarHandler(),
                                                      Util.util.random_color(), self.n_players),
            1: Drawable.DrawablePlayer.DrawablePlayer(1, self.board, DijkstraHandler(),
                                                      Util.util.random_color(), self.n_players),
            2: Drawable.DrawablePlayer.DrawablePlayer(2, self.board, BellmanFordHandler(),
                                                      Util.util.random_color(), self.n_players),
            3: Drawable.DrawablePlayer.DrawablePlayer(3, self.board, FloydWarshallHandler(),
                                                      Util.util.random_color(), self.n_players)
        }

        if self.n_players == 2:
            del self.players[1]
            del self.players[3]

    def draw(self, screen):
        self.board.draw(screen)
        self.board.draw_barriers(screen)
        for player in self.players.values():
            player.draw(self.board, screen)

    def start(self):
        screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]))
        pygame.display.set_caption('Final project')

        pygame.init()

        done = False
        winner = None

        if self.n_players == 2:
            current = choice([0, 2])
        else:
            current = choice([0, 1, 2, 3])

        while not done:
            current_player = self.players[current]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            current_player.decide(self.board, Util.util.get_player_opponent(current_player, self.players))

            screen.fill((255, 255, 255))
            self.draw(screen)
            pygame.display.flip()
            pygame.time.delay(200)

            if current_player.is_in_winning_position():
                winner = current_player
                done = True

            if self.n_players == 4:
                current = (current + 1) % self.n_players
            else:
                if current == 0:
                    current = 2
                else:
                    current = 0

        if winner:
            print(winner.n)
        pygame.quit()

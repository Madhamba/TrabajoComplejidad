import pygame


class Square:
    def __init__(self, pos, width, height, color):
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        info = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, info, 2)

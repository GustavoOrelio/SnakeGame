import pygame


class Object:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def draw(self, window, size, rows):
        pygame.draw.rect(window, self.color,
                         (self.pos[0] * size // rows, self.pos[1] * size // rows, size // rows, size // rows))

import pygame

from Object import Object


class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.body = [Object(color, pos)]
        self.direction = pygame.K_RIGHT

    def move(self):
        head = self.body[0]
        if self.direction == pygame.K_UP:
            head.pos = (head.pos[0], head.pos[1] - 1)
        elif self.direction == pygame.K_DOWN:
            head.pos = (head.pos[0], head.pos[1] + 1)
        elif self.direction == pygame.K_LEFT:
            head.pos = (head.pos[0] - 1, head.pos[1])
        elif self.direction == pygame.K_RIGHT:
            head.pos = (head.pos[0] + 1, head.pos[1])

    def draw(self, window, size, rows):
        for part in self.body:
            part.draw(window, size, rows)

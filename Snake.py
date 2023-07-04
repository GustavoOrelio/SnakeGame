import pygame

from Object import Object


class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.body = [Object(color, pos)]
        self.direction = pygame.K_RIGHT

    def move(self):
        head = self.body[0].pos
        if self.direction == pygame.K_UP:
            new_pos = (head[0], head[1] - 1)
        elif self.direction == pygame.K_DOWN:
            new_pos = (head[0], head[1] + 1)
        elif self.direction == pygame.K_LEFT:
            new_pos = (head[0] - 1, head[1])
        elif self.direction == pygame.K_RIGHT:
            new_pos = (head[0] + 1, head[1])
        else:
            return
        self.body.insert(0, Object(self.color, new_pos))
        self.body.pop()

    def grow(self):
        tail = self.body[-1].pos
        self.body.append(Object(self.color, tail))

    def draw(self, window, size, rows):
        for part in self.body:
            part.draw(window, size, rows)

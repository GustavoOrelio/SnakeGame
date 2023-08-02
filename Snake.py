import pygame

from Object import Object
from Position import Position


class Snake(Object):
    def __init__(self, head_sprite, body_sprite, position, size):
        super().__init__(head_sprite, position, size)
        self.body_sprite = body_sprite
        self.body = [self]
        self.direction = pygame.K_RIGHT
        self.size = size  # Add this line

    def move(self, rows):
        head = self.body[0].position
        if self.direction == pygame.K_UP:
            new_pos = Position(head.x, head.y - 1)
        elif self.direction == pygame.K_DOWN:
            new_pos = Position(head.x, head.y + 1)
        elif self.direction == pygame.K_LEFT:
            new_pos = Position(head.x - 1, head.y)
        elif self.direction == pygame.K_RIGHT:
            new_pos = Position(head.x + 1, head.y)
        else:
            return
        self.body.insert(0, Object(self.body_sprite, new_pos, self.size))  # Pass size here
        self.body.pop()

    def grow(self):
        tail = self.body[-1].position
        self.body.append(Object(self.body_sprite, tail, self.size))

    def draw(self, window, size, rows):
        for part in self.body:
            part.draw(window, size, rows)

    def collides_with_wall(self, rows):
        head = self.body[0].position
        return head.x < 0 or head.y < 0 or head.x >= rows or head.y >= rows

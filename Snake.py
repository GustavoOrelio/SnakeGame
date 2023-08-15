import pygame

from Object import Object
from Position import Position


class Snake:
    def __init__(self, sprite_path, position, size):
        self.head_sprite, self.body_straight_sprite, self.body_curve_sprite, self.tail_sprite = self.load_sprite(
            sprite_path, size)

        self.body = [Object(self.head_sprite, position, size)]
        self.direction = pygame.K_RIGHT
        self.size = size

    def load_sprite(self, sprite_path, size):
        full_sprite = pygame.image.load(sprite_path)

        head = full_sprite.subsurface((0, 0, size, size))
        head = pygame.transform.scale(head, (self.sprite_size, self.sprite_size))

        body_straight = full_sprite.subsurface((size, 0, size, size))
        body_straight = pygame.transform.scale(body_straight, (self.sprite_size, self.sprite_size))

        body_curve = full_sprite.subsurface((2 * size, 0, size, size))
        body_curve = pygame.transform.scale(body_curve, (self.sprite_size, self.sprite_size))

        tail = full_sprite.subsurface((3 * size, 0, size, size))
        tail = pygame.transform.scale(tail, (self.sprite_size, self.sprite_size))

        return head, body_straight, body_curve, tail

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

        self.body.insert(0, Object(self.body_straight_sprite, new_pos, self.size))
        self.body.pop()

    def grow(self):
        tail = self.body[-1].position
        self.body.append(Object(self.tail_sprite, tail, self.size))

    def draw(self, window, size, rows):
        # Desenhar a cabeça
        window.blit(self.head_sprite, (self.body[0].position.x * size // rows, self.body[0].position.y * size // rows))

        # Desenhar o corpo (se houver mais de um segmento)
        for i in range(1, len(self.body) - 1):
            window.blit(self.body_straight_sprite,
                        (self.body[i].position.x * size // rows, self.body[i].position.y * size // rows))

        # Desenhar a cauda (se houver mais de um segmento)
        if len(self.body) > 1:
            window.blit(self.tail_sprite,
                        (self.body[-1].position.x * size // rows, self.body[-1].position.y * size // rows))

    def collides_with_wall(self, rows):
        head = self.body[0].position
        return head.x < 0 or head.y < 0 or head.x >= rows or head.y >= rows

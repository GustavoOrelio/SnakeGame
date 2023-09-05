import pygame

from Position import Position
from SnakeSegment import SnakeSegment


class Snake:
    def __init__(self, sprite_paths, position, size):
        self.sprite_size = size
        self.load_sprites(sprite_paths, size)

        # A cobra começa com um segmento de cabeça e um de cauda
        self.body = [
            SnakeSegment(self.sprites['head'], position, size, pygame.K_RIGHT),
            SnakeSegment(self.sprites['cauda'], Position(position.x - 1, position.y), size, pygame.K_RIGHT)
        ]

        self.direction = pygame.K_RIGHT
        self.should_grow = False

    def load_sprites(self, sprite_paths, size):
        self.sprites = {}
        for key, path in sprite_paths.items():
            loaded_sprite = pygame.image.load(path)
            self.sprites[key] = pygame.transform.scale(loaded_sprite, (self.sprite_size, self.sprite_size))

    def move(self, rows):
        # Atualizar a direção anterior de todos os segmentos
        for segment in self.body:
            segment.prev_direction = segment.direction
        head = self.body[0].position
        new_direction = self.direction
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

        if self.should_grow:
            self.grow()
            self.should_grow = False

        # Cria um novo segmento de cabeça e o adiciona ao corpo
        new_head = SnakeSegment(self.sprites['head'], new_pos, self.sprite_size, new_direction)
        self.body.insert(0, new_head)

        # Remove a cauda antiga
        self.body.pop()

    def grow(self):
        tail = self.body[-1].position
        tail_direction = self.body[-1].direction
        self.body.append(SnakeSegment(self.sprites['cauda'], tail, self.sprite_size, tail_direction))

    def draw(self, window, size, rows):
        curve_added = False
        for i in range(len(self.body)):
            segment = self.body[i]
            rotation_angle = 0
            sprite_type = 'body'  # Assume-se que o segmento é do corpo por padrão

            if i == 0:
                sprite_type = 'head'
            elif i == len(self.body) - 1:
                sprite_type = 'cauda'
            else:
                prev_direction = self.body[i - 1].direction
                next_direction = self.body[i + 1].direction
                if prev_direction != next_direction and not curve_added and len(self.body) > 2:
                    curve_added = True

                    if (prev_direction == pygame.K_UP and next_direction == pygame.K_RIGHT) or \
                            (prev_direction == pygame.K_LEFT and next_direction == pygame.K_DOWN):
                        sprite_type = 'curve_right'
                    else:
                        sprite_type = 'curve_left'

            if segment.direction == pygame.K_UP:
                rotation_angle = 0
            elif segment.direction == pygame.K_DOWN:
                rotation_angle = 180
            elif segment.direction == pygame.K_LEFT:
                rotation_angle = 90
            elif segment.direction == pygame.K_RIGHT:
                rotation_angle = -90

            rotated_sprite = pygame.transform.rotate(self.sprites[sprite_type], rotation_angle)
            segment.sprite = rotated_sprite
            segment.draw(window, size, rows)

    def collides_with_wall(self, rows):
        head = self.body[0].position
        return head.x < 0 or head.y < 0 or head.x >= rows or head.y >= rows

    def collides_with_self(self):
        head = self.body[0].position
        for segment in self.body[1:]:
            if head.x == segment.position.x and head.y == segment.position.y:
                return True
        return False

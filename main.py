import random

import pygame


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Object:
    def __init__(self, sprite_input, position, size):
        if isinstance(sprite_input, pygame.Surface):
            self.sprite = pygame.transform.scale(sprite_input, (size, size))
        else:
            loaded_sprite = pygame.image.load(sprite_input)
            self.sprite = pygame.transform.scale(loaded_sprite, (size, size))
        self.position = position

    def draw(self, window, size, rows):
        window.blit(self.sprite, (self.position.x * size // rows, self.position.y * size // rows))

    def collides_with(self, other):
        return self.position.x == other.position.x and self.position.y == other.position.y


class SnakeSegment(Object):
    def __init__(self, sprite_input, position, size, direction):
        super().__init__(sprite_input, position, size)
        self.direction = direction  # direção atual deste segmento
        self.prev_direction = direction  # direção anterior deste segmento


class Snake:
    def __init__(self, sprite_paths, position, size):
        self.sprite_size = size
        self.load_sprites(sprite_paths, size)
        self.body = [SnakeSegment(self.sprites['head'], position, size, pygame.K_RIGHT)]
        self.direction = pygame.K_RIGHT

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
        for i in range(len(self.body)):
            segment = self.body[i]
            rotation_angle = 0

            if segment.direction == pygame.K_UP:
                rotation_angle = 0
            elif segment.direction == pygame.K_DOWN:
                rotation_angle = 180
            elif segment.direction == pygame.K_LEFT:
                rotation_angle = 90
            elif segment.direction == pygame.K_RIGHT:
                rotation_angle = -90

            # Verifique se é uma curva e se o corpo tem mais de 2 segmentos.
            if 0 < i < len(self.body) - 1 and len(self.body) > 2:
                prev_direction = self.body[i - 1].direction
                next_direction = self.body[i + 1].direction

                if prev_direction != next_direction:
                    # Uma curva está acontecendo.
                    if self.direction == prev_direction:
                        # A cobra está virando em direção a next_direct
                        # ion.
                        rotated_sprite = pygame.transform.rotate(self.sprites['curve_right'], rotation_angle)
                    else:
                        # A cobra está virando em direção a prev_direction.
                        rotated_sprite = pygame.transform.rotate(self.sprites['curve_left'], rotation_angle)
                else:
                    rotated_sprite = pygame.transform.rotate(self.sprites['body'], rotation_angle)
            elif i == 0:
                rotated_sprite = pygame.transform.rotate(self.sprites['head'], rotation_angle)
            else:
                rotated_sprite = pygame.transform.rotate(self.sprites['cauda'], rotation_angle)

            segment.sprite = rotated_sprite
            segment.draw(window, size, rows)

    def collides_with_wall(self, rows):
        head = self.body[0].position
        return head.x < 0 or head.y < 0 or head.x >= rows or head.y >= rows


class Game:
    def __init__(self, size, rows, sprite_paths):
        pygame.init()
        self.size = size
        self.rows = rows
        self.window = pygame.display.set_mode((size, size))
        self.sprite_size = size // rows
        self.snake = Snake(sprite_paths, Position(10, 10), self.sprite_size)
        self.apple = Object("img/apple.png", Position(random.randint(0, rows - 1), random.randint(0, rows - 1)),
                            self.sprite_size)

    def grid(self):
        distanceBtwRows = self.size // self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x += distanceBtwRows
            y += distanceBtwRows
            pygame.draw.line(self.window, (255, 255, 255), (x, 0), (x, self.size))
            pygame.draw.line(self.window, (255, 255, 255), (0, y), (self.size, y))

    def redraw(self):
        self.window.fill((0, 0, 0))
        self.grid()
        self.snake.draw(self.window, self.size, self.rows)
        self.apple.draw(self.window, self.size, self.rows)
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != pygame.K_DOWN:
                    self.snake.direction = event.key
                elif event.key == pygame.K_DOWN and self.snake.direction != pygame.K_UP:
                    self.snake.direction = event.key
                elif event.key == pygame.K_LEFT and self.snake.direction != pygame.K_RIGHT:
                    self.snake.direction = event.key
                elif event.key == pygame.K_RIGHT and self.snake.direction != pygame.K_LEFT:
                    self.snake.direction = event.key

    def check_collisions(self):
        if self.snake.collides_with_wall(self.rows):
            print("Game Over!")
            exit()
        if self.snake.body[0].collides_with(self.apple):
            self.apple.position = Position(random.randint(0, self.rows - 1), random.randint(0, self.rows - 1))
            self.snake.grow()

    def play(self):
        while True:
            pygame.time.delay(200)
            self.handle_events()
            self.snake.move(self.rows)
            self.check_collisions()
            self.redraw()


if __name__ == "__main__":
    sprite_paths = {
        'head': 'img/snake_head.png',
        'body': 'img/snake_body.png',
        'cauda': 'img/snake_cauda.png',
        'curve_left': 'img/snake_curve_left.png',
        'curve_right': 'img/snake_curve_right.png'
    }
    game = Game(500, 20, sprite_paths)
    game.play()

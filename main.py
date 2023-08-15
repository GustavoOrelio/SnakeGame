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


class Snake:
    def __init__(self, sprite_path, position, size):
        self.sprite_size = size
        self.head_sprite, self.body_sprite, self.tail_sprite = self.load_sprite(sprite_path, size)
        self.body = [Object(self.head_sprite, position, size)]
        self.direction = pygame.K_RIGHT

    def load_sprite(self, sprite_path, size):
        full_sprite = pygame.image.load(sprite_path)

        head = full_sprite.subsurface((0, 0, size, size))
        head = pygame.transform.scale(head, (self.sprite_size, self.sprite_size))

        body = full_sprite.subsurface((size, 0, size, size))
        body = pygame.transform.scale(body, (self.sprite_size, self.sprite_size))

        tail = full_sprite.subsurface((2 * size, 0, size, size))
        tail = pygame.transform.scale(tail, (self.sprite_size, self.sprite_size))

        return head, body, tail

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

        self.body.insert(0, Object(self.head_sprite, new_pos, self.sprite_size))
        self.body.pop()
        for i in range(1, len(self.body) - 1):
            self.body[i].sprite = self.body_sprite

    def grow(self):
        tail = self.body[-1].position
        self.body.append(Object(self.tail_sprite, tail, self.sprite_size))

    def draw(self, window, size, rows):
        for part in self.body:
            part.draw(window, size, rows)

    def collides_with_wall(self, rows):
        head = self.body[0].position
        return head.x < 0 or head.y < 0 or head.x >= rows or head.y >= rows


class Game:
    def __init__(self, size, rows):
        pygame.init()
        self.size = size
        self.rows = rows
        self.window = pygame.display.set_mode((size, size))
        self.sprite_size = size // rows
        self.snake = Snake("img/sprite_snake.png", Position(10, 10), self.sprite_size)
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
            pygame.time.delay(100)
            self.handle_events()
            self.snake.move(self.rows)
            self.check_collisions()
            self.redraw()


if __name__ == "__main__":
    game = Game(500, 20)
    game.play()

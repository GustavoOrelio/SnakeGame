import random

import pygame

from Object import Object
from Position import Position
from Snake import Snake


class Game:
    def __init__(self, size, rows):
        self.size = size
        self.rows = rows
        self.window = pygame.display.set_mode((size, size))
        self.sprite_size = size // rows  # Calculate the size of the sprites
        self.snake = Snake("img/snake_sprite.png", Position(10, 10), self.sprite_size)
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
            self.apple.position = Position(random.randint(0, self.rows - 1),
                                           random.randint(0, self.rows - 1))
            self.snake.grow()

    def play(self):
        while True:
            pygame.time.delay(100)
            self.handle_events()
            self.snake.move(self.rows)
            self.check_collisions()
            self.redraw()

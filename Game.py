import pygame
import random

from Object import Object
from Snake import Snake


class Game:
    def __init__(self, size, rows):
        self.size = size
        self.rows = rows
        self.window = pygame.display.set_mode((size, size))
        self.snake = Snake((0, 255, 0), (10, 10))
        self.apple = Object((255, 0, 0), (random.randint(0, rows - 1), random.randint(0, rows - 1)))

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

    def play(self):
        while True:
            pygame.time.delay(100)
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
            self.snake.move()
            # Verificando se a cobra colidiu com a borda da tela
            if (self.snake.body[0].pos[0] < 0 or self.snake.body[0].pos[0] >= self.rows or
                    self.snake.body[0].pos[1] < 0 or self.snake.body[0].pos[1] >= self.rows):
                print("Você perdeu: Colidiu com a borda")
                return
            # Verificando se a cobra colidiu nela mesmo
            if self.snake.body[0].pos in [part.pos for part in self.snake.body[1:]]:
                print("Você perdeu: Colidiu com seu corpo")
                return
            if self.snake.body[0].pos == self.apple.pos:
                self.apple.pos = (random.randint(0, self.rows - 1), random.randint(0, self.rows - 1))
                self.snake.grow()
            self.redraw()

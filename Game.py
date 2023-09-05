import random

import pygame

from Object import Object
from Position import Position
from Snake import Snake


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
        self.score = 0  # Inicializar a pontuação

    def grid(self):
        distanceBtwRows = self.size // self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x += distanceBtwRows
            y += distanceBtwRows
            # pygame.draw.line(self.window, (255, 255, 255), (x, 0), (x, self.size))
            # pygame.draw.line(self.window, (255, 255, 255), (0, y), (self.size, y))

    def redraw(self):
        self.window.fill((0, 0, 0))
        self.grid()
        self.snake.draw(self.window, self.size, self.rows)
        self.apple.draw(self.window, self.size, self.rows)
        self.show_score()  # Mostrar a pontuação
        pygame.display.update()

    # Método para exibir a pontuação
    def show_score(self):
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.window.blit(score_surface, (10, 10))

    def check_collisions(self):
        # Verifique se a cobra colide com as paredes
        if self.snake.collides_with_wall(self.rows):
            if not self.game_over_screen():
                exit()

        # Verifique se a cobra colide com ela mesma
        if self.snake.collides_with_self():
            if not self.game_over_screen():
                exit()

        if self.snake.body[0].collides_with(self.apple):
            self.apple.position = Position(random.randint(0, self.rows - 1), random.randint(0, self.rows - 1))
            self.snake.should_grow = True
            self.score += 1  # Aumentar a pontuação

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

    def game_over_screen(self):
        font = pygame.font.Font(None, 74)
        game_over = font.render('Game Over', True, (255, 0, 0))
        retry = font.render('Retry? (y/n)', True, (255, 255, 255))

        self.window.blit(game_over, [self.size // 4, self.size // 3])
        self.window.blit(retry, [self.size // 4, self.size // 2])

        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        print("User chose to retry")
                        waiting_for_input = False
                        return True
                    if event.key == pygame.K_n:
                        print("User chose to exit")
                        waiting_for_input = False
                        return False

    def play(self):
        while True:
            pygame.time.delay(150)
            self.handle_events()
            self.snake.move(self.rows)
            self.check_collisions()
            self.redraw()

            if self.snake.collides_with_wall(self.rows) or self.snake.collides_with_self():
                retry = self.game_over_screen()
                print(f"Retry is {retry}")
                return retry

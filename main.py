import random

import pygame

from Object import Object
from Snake import Snake


def grid(window, size, rows):
    distanceBtwRows = size // rows
    x = 0
    y = 0
    for l in range(rows):
        x += distanceBtwRows
        y += distanceBtwRows

        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, size))
        pygame.draw.line(window, (255, 255, 255), (0, y), (size, y))


def redraw(window, snake, apple):
    window.fill((0, 0, 0))
    grid(window, size, rows)
    snake.draw(window, size, rows)
    apple.draw(window, size, rows)
    pygame.display.update()


def main():
    global size, rows
    size = 500
    rows = 20
    window = pygame.display.set_mode((size, size))
    snake = Snake((0, 255, 0), (10, 10))
    apple = Object((255, 0, 0), (random.randint(0, rows - 1), random.randint(0, rows - 1)))

    color = snake.color
    r = color[0]
    g = color[1]
    b = color[2]
    print(g)

    pos = snake.body[0].pos
    x = pos[0]
    y = pos[1]
    print(x)

    play = True

    while play:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.direction = event.key
        snake.move()
        if snake.body[0].pos == apple.pos:
            apple.pos = (random.randint(0, rows - 1), random.randint(0, rows - 1))
            snake.body.append(Object(snake.color, snake.body[-1].pos))
        redraw(window, snake, apple)


main()

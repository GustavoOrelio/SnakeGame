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

    def play(self):
        while True:
            pygame.time.delay(200)
            self.handle_events()
            self.snake.move(self.rows)
            self.check_collisions()
            self.redraw()

            if self.snake.collides_with_wall(self.rows) or self.snake.collides_with_self():
                retry = self.game_over_screen()
                print(f"Retry is {retry}")
                return retry


def main_game():
    sprite_paths = {
        'head': 'img/snake_head.png',
        'body': 'img/snake_body.png',
        'cauda': 'img/snake_cauda.png',
        'curve_left': 'img/snake_curve.png',
        'curve_right': 'img/snake_curve_right.png'
    }
    game = Game(500, 20, sprite_paths)
    retry = game.play()
    print(f"Main game retry is {retry}")
    return retry


if __name__ == "__main__":
    retry = True
    while retry:
        print("Starting a new game")
        retry = main_game()

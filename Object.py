import pygame


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

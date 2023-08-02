import pygame


class Object:
    def __init__(self, sprite, position, size):
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, (size, size))  # Redimensiona a imagem
        self.position = position

    def draw(self, window, size, rows):
        window.blit(self.sprite, (self.position.x * size // rows, self.position.y * size // rows))

    def collides_with(self, other):
        return self.position.x == other.position.x and self.position.y == other.position.y

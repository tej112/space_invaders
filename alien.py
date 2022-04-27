import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        filepath = './Space-invaders-main/graphics/' + color + '.png'
        self.image = pygame.image.load(filepath).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction

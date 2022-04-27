import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed=5):
        super().__init__()
        self.image = pygame.image.load("./Space-invaders-main/graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 800

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def check_constraint(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.midtop, self.rect.bottom))

    def recharge_laser(self):
        if not self.ready:
            if pygame.time.get_ticks() - self.laser_time > self.laser_cooldown:
                self.ready = True

    def update(self):
        self.get_input()
        self.check_constraint()
        self.recharge_laser()
        self.lasers.update()

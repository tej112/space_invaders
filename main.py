from random import choice
import pygame
import sys
from laser import Laser
from player import Player
import obstacle
from alien import Alien


class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2, screen_height), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.score = 0
        self.font = pygame.font.Font('./Space-invaders-main/font/Pixeled.ttf', 20)

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(6, 8, x_distance=60, y_distance=48, x_offset=70, y_offset=100)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (200, 200, 200), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance, y_distance, x_offset, y_offset):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien = Alien('green', x, y)
                else:
                    alien = Alien('red', x, y)
                self.aliens.add(alien)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.left < 0:
                self.alien_direction = 1
                self.move_aliens_down(1)
            if alien.rect.right > screen_width:
                self.alien_direction = -1
                self.move_aliens_down(1)

    def move_aliens_down(self, distance):
        if self.aliens.sprites():
            for alien in self.aliens:
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, screen_height, -8)
            self.alien_lasers.add(laser_sprite)

    def collison_check(self):
        # player Lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    self.score += 100
                    laser.kill()
        # Alien Lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    pygame.quit()
                    sys.exit()

        # Aliens Itself
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_score(self):
        score_surf = self.font.render(f"Score:{self.score}", False, 'white')
        score_rect = score_surf.get_rect(topleft = (10, - 10))
        screen.blit(score_surf, score_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.collison_check()
        self.display_score()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        if len(self.aliens) == 0:
            screen.fill('black')
            self.font = pygame.font.Font('freesansbold.ttf', 32)
            score_surf = self.font.render("You Won!", True, 'white')
            score_rect = score_surf.get_rect(center=(300, 275))
            screen.blit(score_surf, score_rect)
            pygame.display.update()
            score_surf = self.font.render(f"Score: {self.score}", True, 'white')
            score_rect = score_surf.get_rect(center=(300, 325))
            screen.blit(score_surf, score_rect)
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        screen.fill((30, 30, 30))
        game.run()
        pygame.display.update()
        clock.tick(60)

import math
import pygame
from config import *
from pygame.locals import *


class ProjectTile(pygame.sprite.Sprite):
    def __init__(self, gun_angle):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.gun_angle = gun_angle
        self.speed = 5

        pygame.draw.circle(self.image, (255, 255, 0), (self.rect.centerx, self.rect.centery), 10)

    def update(self, dt):
        # pygame.draw.circle(self.image, (255, 255, 0), (self.rect.centerx, self.rect.centery), 25)

        gun_angle = (self.gun_angle - 90) * (math.pi / 180)
        self.rect.move_ip(self.speed * math.sin(gun_angle) * dt, self.speed * math.cos(gun_angle) * dt)

        if (self.rect.left > SCREEN_SIZE[0]) or \
                (self.rect.right < 0) or \
                (self.rect.top > SCREEN_SIZE[1]) or \
                (self.rect.bottom < 0):
            self.kill()


class EnemyAutoGun(pygame.sprite.Sprite):
    def __init__(self, name, group, images_paths, players, game_surf, all_sprites_list, width=None, height=None):
        super().__init__()

        self.name = name
        self.group = group
        self.width = width
        self.height = height
        self.images_paths = images_paths
        self.players = players
        self.player = None
        self.game_surf = game_surf

        self.stand_image = pygame.image.load(self.images_paths[0]).convert()
        self.stand_rect = self.stand_image.get_rect()
        self.gun_image = pygame.image.load(self.images_paths[1]).convert()
        self.gun_rect = self.gun_image.get_rect()

        self.image = pygame.Surface((100, 100))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.stand_rect.centerx = self.rect.centerx
        self.stand_rect.bottom = self.rect.bottom
        # self.gun_rect.centerx = self.rect.centerx
        # self.gun_rect.centery = self.stand_rect.centery
        self.gun_mount_point = (self.stand_rect.centerx, self.stand_rect.centery - 25)

        self.player_angle = 0
        self.gun_angle = 0
        self.reaction_speed = 0.2
        self.range = 800
        self.gun_timer = 0
        self.project_tiles = pygame.sprite.Group()
        all_sprites_list.append(self.project_tiles)

        self.offset = 200
        self.screen_center_pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

    def update(self, dt):
        if self.player is None:
            self.player = self.players.sprites()[0] if len(self.players) > 0 else None

        self.image.fill(COLOR_SKY)
        self.image.set_colorkey(COLOR_SKY)
        rotated_gun_image = pygame.transform.rotate(self.gun_image, self.gun_angle)
        rotated_gun_image.set_colorkey(WHITE)
        new_gun_rect = rotated_gun_image.get_rect(center=self.gun_image.get_rect(center=self.gun_mount_point).center)

        self.image.blit(rotated_gun_image, new_gun_rect)
        self.image.blit(self.stand_image, self.stand_rect)

        if len(self.players) > 0:
            player_distance_x = self.rect.centerx - self.player.rect.centerx
            player_distance_y = self.rect.centery - self.player.rect.centery
            self.player_angle = -math.atan2(player_distance_y, player_distance_x) * (180 / math.pi)

            if math.sqrt((player_distance_x ** 2) + (player_distance_y ** 2)) < self.range:
                if self.gun_angle < self.player_angle:
                    self.gun_angle += self.reaction_speed * dt
                elif self.gun_angle > self.player_angle:
                    self.gun_angle -= self.reaction_speed * dt

                self.gun_timer += 1 * dt

                if self.gun_timer >= 75:
                    project_tile = ProjectTile(self.gun_angle)
                    project_tile.rect.centerx = self.rect.centerx
                    project_tile.rect.centery = self.rect.centery
                    self.project_tiles.add(project_tile)

                    self.gun_timer = 0

        self.project_tiles.update(dt)
        self.project_tiles.draw(self.game_surf)

import math
import pygame
from config import *
from pygame.locals import *


class EnemyAutoGun(pygame.sprite.Sprite):
    def __init__(self, name, group, images_paths, players, width=None, height=None):
        super().__init__()

        self.name = name
        self.group = group
        self.width = width
        self.height = height
        self.images_paths = images_paths
        self.players = players
        self.player = None

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
        self.gun_mount_point = (self.stand_rect.centerx, self.stand_rect.centery - 20)

        self.player_angle = 0
        self.gun_angle = 0
        self.reaction_speed = 0.3
        self.range = 700

    def update(self, dt):
        if self.player is None:
            self.player = self.players.sprites()[0] if len(self.players) > 0 else None

        self.image.fill(COLOR_SKY)
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

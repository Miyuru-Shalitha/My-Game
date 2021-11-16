import pygame
from pygame.locals import *
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, group, image_path, width=None, height=None):
        super().__init__()
        self.group = group
        self.width = width
        self.height = height

        self.image_path = image_path
        self.image = self.get_sprite()

        self.rect = self.image.get_rect()
        self.speed = 5

    def get_sprite(self):
        surf = pygame.Surface([64, 64])
        surf.set_colorkey(BLACK)
        sprite_sheet_surf = pygame.image.load(self.image_path).convert()
        sprite_sheet_surf.set_colorkey(WHITE)
        surf.blit(sprite_sheet_surf, (0, 0), (0, 0, 64, 64))

        if (self.width is not None) and (self.height is not None):
            surf = pygame.transform.scale(surf, (self.width, self.height))

        return surf

    def update(self, pressed_keys):
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.speed

        if pressed_keys[K_LEFT]:
            self.rect.x -= self.speed

        if pressed_keys[K_UP]:
            self.rect.y -= self.speed

        if pressed_keys[K_DOWN]:
            self.rect.y += self.speed

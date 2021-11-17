import pygame
from config import *
from game_physics import GravityMixin, ColliderMixin
from pygame.locals import *


class Player(pygame.sprite.Sprite, GravityMixin, ColliderMixin):
    def __init__(self, group, image_path, width=None, height=None, rigid_objects=()):
        super().__init__()
        super(pygame.sprite.Sprite, self).__init__(self)
        super(GravityMixin, self).__init__(self, rigid_objects, self.y_change)

        self.group = group
        self.width = width
        self.height = height

        self.image_path = image_path
        self.image = self.get_sprite()
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.speed = 5
        self.y_change = 0
        self.is_grounded = False

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

        # self.apply_gravity()
        self.apply_collisions()

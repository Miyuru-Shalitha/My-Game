import pygame
from config import *
from game_physics import GravityMixin, ColliderMixin
from pygame.locals import *


class Player(pygame.sprite.Sprite, GravityMixin):
    def __init__(self, group, image_path, width=None, height=None, rigid_objects_groups=()):
        super().__init__()
        super(pygame.sprite.Sprite, self).__init__(self)

        self.group = group
        self.width = width
        self.height = height
        self.rigid_objects_groups = rigid_objects_groups

        self.image_path = image_path
        self.image = self.get_sprite()
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.speed = 5
        self.jump_force = 10
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

            for objs_group in self.rigid_objects_groups:
                for block in pygame.sprite.spritecollide(self, objs_group, False):
                    if self.rect.right > block.rect.left:
                        self.rect.right = block.rect.left

        if pressed_keys[K_LEFT]:
            self.rect.x -= self.speed

            for objs_group in self.rigid_objects_groups:
                for block in pygame.sprite.spritecollide(self, objs_group, False):
                    if self.rect.left < block.rect.right:
                        self.rect.left = block.rect.right

        if pressed_keys[K_UP] and self.is_grounded:
            self.y_change = -self.jump_force
            self.is_grounded = False

        ###########################################################################
        self.apply_gravity()

        if self.y_change > 1:
            self.is_grounded = False

        if (not self.is_grounded) and (self.y_change < 0):
            for objs_group in self.rigid_objects_groups:
                for block in pygame.sprite.spritecollide(self, objs_group, False):
                    if self.rect.top < block.rect.bottom:
                        self.y_change = 0
                        self.rect.top = block.rect.bottom

        for objs_group in self.rigid_objects_groups:
            for block in pygame.sprite.spritecollide(self, objs_group, False):
                if self.rect.bottom > block.rect.top:
                    self.y_change = 0
                    self.is_grounded = True
                    self.rect.bottom = block.rect.top

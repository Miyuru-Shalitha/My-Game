import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 40])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.speed = 1
        # self.rect.centerx = 500
        # self.rect.centery = 500

    def update(self, pressed_keys):
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.speed

        if pressed_keys[K_LEFT]:
            self.rect.x -= self.speed

        if pressed_keys[K_UP]:
            self.rect.y -= self.speed

        if pressed_keys[K_DOWN]:
            self.rect.y += self.speed

        print(self.rect.x, self.rect.y)

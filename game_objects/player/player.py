import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, width=None, height=None):
        super().__init__()
        self.width = width
        self.height = height

        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert()

        if (self.width is not None) and (self.height is not None):
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self, pressed_keys):
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.speed

        if pressed_keys[K_LEFT]:
            self.rect.x -= self.speed

        if pressed_keys[K_UP]:
            self.rect.y -= self.speed

        if pressed_keys[K_DOWN]:
            self.rect.y += self.speed

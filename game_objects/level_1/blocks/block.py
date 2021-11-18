import pygame
from pygame.locals import *


class Block(pygame.sprite.Sprite):
    def __init__(self, name, group, image_path, width=None, height=None):
        super().__init__()
        self.name = name
        self.group = group
        self.width = width
        self.height = height

        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert()

        if (self.width is not None) and (self.height is not None):
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()

    def update(self):
        pass

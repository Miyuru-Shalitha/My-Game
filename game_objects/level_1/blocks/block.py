import pygame
from config import *
from pygame.locals import *


class Block(pygame.sprite.Sprite):
    def __init__(self, name, group, image_path, width=None, height=None, flip_x=None, flip_y=None, angle=None):
        super().__init__()
        self.name = name
        self.group = group
        self.width = width
        self.height = height
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.angle = angle

        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert()

        if (self.flip_x is not None) and (self.flip_y is not None):
            self.image = pygame.transform.flip(self.image, self.flip_x, self.flip_y)

        if self.angle is not None:
            self.image = pygame.transform.rotate(self.image, self.angle)

        self.image.set_colorkey(WHITE)

        if (self.width is not None) and (self.height is not None):
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()

    def update(self):
        pass

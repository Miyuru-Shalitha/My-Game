import pygame
from pygame.locals import *


class Grass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

    def update(self):
        pass

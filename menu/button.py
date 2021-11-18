import pygame
from pygame.locals import *


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image_path, func, width=None, height=None):
        super().__init__()
        self.group = group
        self.width = width
        self.height = height

        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert()

        self.func = func

        if (self.width is not None) and (self.height is not None):
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()

    def update(self, mouse_x, mouse_y, clicked_mouse_buttons):
        if clicked_mouse_buttons[0]:
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.func()

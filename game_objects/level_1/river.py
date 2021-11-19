import pygame
import random
from config import *
from pygame.locals import *


class River(pygame.sprite.Sprite):
    def __init__(self, name, group, image_path, width=None, height=None):
        super().__init__()
        self.name = name
        self.group = group
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(COLOR_SKY)
        self.image_path = image_path
        self.river_image = pygame.image.load(image_path).convert()
        self.river_image.set_colorkey(WHITE)

        if (self.width is not None) and (self.height is not None):
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()

        self.water_particles = []

    def update(self, dt):
        self.image.fill(COLOR_SKY)
        self.image.blit(self.river_image, (0, 0))

        # Particles ##############################
        for _ in range(100):
            self.water_particles.append([
                [random.uniform(0, self.width), 10],
                [random.uniform(-2, 2), 0.5, 0.1],
                [random.randint(5, 10), -0.01]
            ])

        for particle in self.water_particles:
            if (particle[2][0] <= 0) or \
                    (particle[0][0] > self.width) or \
                    (particle[0][0] < 0) or \
                    (particle[0][1] > self.height):
                self.water_particles.remove(particle)

        for particle in self.water_particles:
            pygame.draw.circle(self.image, COLOR_WATER, particle[0], particle[2][0])

            particle[0][0] += particle[1][0] * dt
            particle[1][1] += particle[1][2] * dt
            particle[0][1] += particle[1][1] * dt
            particle[2][0] += particle[2][1] * dt
        ##########################################

import pygame
import os
from constants import *


# BIRD = pygame.image.load(os.path.join("imgs", "bird1.png"))

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.6
        self.vel = 0;
        self.lift = 5
        self.crashed = False
        self.bird = BIRD2
        self.rotation = 0
        self.max_rotation = 90
        self.animation = 0
        self.a_time = 10 # animation_time

    def draw(self, win):
        self.animation += 1
        if self.animation == 1 * self.a_time:
            self.bird = BIRD2
        elif self.animation == 2 * self.a_time:
            self.bird == BIRD3
        elif self.animation == 3 * self.a_time:
            self.bird = BIRD1
            self.animation = 0
        rotated_bird = pygame.transform.rotate(self.bird, self.rotation)
        win.blit(rotated_bird, (self.x, self.y))

    def update(self):
        self.vel += self.gravity
        self.y += self.vel
        self.rotation -= 1.5
        if self.y > HEIGHT:
            self.crashed = True

        if self.y < 0:
            self.y = 0
            self.vel = 0

    def up(self):
        self.vel = -10.5
        self.rotation = 45

    def get_mask(self):
        return pygame.mask.from_surface(self.bird)

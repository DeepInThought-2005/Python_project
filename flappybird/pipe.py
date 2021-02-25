import pygame
import random
from constants import *

class Pipe:
    def __init__(self):
        self.bottom = PIPE
        self.top = pygame.transform.flip(PIPE, False, True)
        self.interval = random.randint(150, 250)
        self.top_height = random.randint(50, HEIGHT // 2)
        self.bottom_height = self.top_height + self.interval
        self.speed = 5
        self.x = WIDTH

    def draw(self, win):
        win.blit(self.top, (self.x, self.top_height - self.top.get_height()))
        win.blit(self.bottom, (self.x, self.bottom_height))

    def update(self):
        self.x -= self.speed

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top)
        bottom_mask = pygame.mask.from_surface(self.bottom)
        top_offset = (self.x - bird.x, self.top_height - self.top.get_height() - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_height - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if b_point or t_point:
            return True
        return False

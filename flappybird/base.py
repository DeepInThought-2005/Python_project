import pygame
from constants import *

class Base:
    def __init__(self, y):
        self.y = y
        self.base = BASE
        self.speed = 5
        self.width = BASE.get_width()
        self.x1 = 0
        self.x2 = WIDTH

    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.base, (self.x1, self.y))
        win.blit(self.base, (self.x2, self.y))

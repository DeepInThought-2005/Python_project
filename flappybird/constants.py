import pygame
import os


WIDTH = 600
HEIGHT = 800


BIRD_WIDTH = 65
BIRD_HEIGHT = 50
BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")), (WIDTH, HEIGHT))
BIRD1 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird1.png")), (BIRD_WIDTH, BIRD_HEIGHT))
BIRD2 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird2.png")), (BIRD_WIDTH, BIRD_HEIGHT))
BIRD3 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird3.png")),(BIRD_WIDTH, BIRD_HEIGHT))
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

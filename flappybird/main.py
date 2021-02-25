import pygame
import os
from bird import *
from constants import *
from pipe import *
from base import *
pygame.font.init()

def draw_window(win, bird, pipes, base, score):
    win.blit(BG, (0, 0))
    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    bird.update()
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
        pipe.update()
    win.blit(text, (WIDTH - text.get_width() - 20, text.get_height()))
    base.move()
    base.draw(win)
    pygame.display.update()

def main():
    score = 0
    pipes = [Pipe()]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappybird")
    bird = Bird(WIDTH // 4, HEIGHT // 2)
    base = Base(HEIGHT - 100)
    run = True
    clock = pygame.time.Clock()
    pipe_interval_time = 80
    pipe_count = 0
    score = 0
    pipe_ind = 0
    while run:
        clock.tick(60)
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].top.get_width():
            pipe_ind = 1
        else:
            pipe_ind = 0

        if pipes[pipe_ind].x == bird.x:
            score += 1

        if bird.y > HEIGHT - 200:
            run = False


        for pipe in pipes:
            if pipe.collide(bird):
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_SPACE]:
                    bird.up()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.up()

        if pipe_count == pipe_interval_time:
            pipes.append(Pipe())
            pipe_count = 0
        if len(pipes) > 2:
            pipes.pop(0)

        draw_window(win, bird, pipes, base, score)
        pipe_count += 1
    main()

main()

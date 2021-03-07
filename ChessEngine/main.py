import pygame
from constants import *
import time
import copy
import random
from board import *
from game import Game

pygame.mixer.init()
pygame.font.init()

a_cool_position = "5B1k/1R6/5p1K/1n1r3p/8/8/8/5b2 w"

def get_square_onclick(m_x, m_y):
    for j in range(8):
        for i in range(8):
            if m_x >= i * W and m_x <= i * W + W and m_y >= j * W and m_y <= j * W + W:
                return i, j

def main():
    def todo_after_move():
        game.valid_moves = []
        game.board.set_every_pos()
        game.selected_pos = ()
        game.board.unselectall()


    win = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    pygame.display.set_caption("ChessL")
    clock = pygame.time.Clock()
    selected = False
    start_time = time.time()

    game = Game()

    run = True
    while run:
        clock.tick(60)
        # if game.gameover:
        #     main()
        if game.started:
            if game.turn == WHITE:
                game.white_time -= time.time() - start_time
            else:
                game.black_time -= time.time() - start_time
            start_time = time.time()
        else:
            start_time = time.time()

        game.draw_window(win)
        game.board.get_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == game.AI_button[2]:
                print("AI")
                if game.AI_AI:
                    game.AI_AI = False
                else:
                    game.AI_AI = True

            if event.type == game.Human_Button[2]:
                print("Human")
                if game.HUMAN_AI:
                    game.HUMAN_AI = False
                else:
                    game.HUMAN_AI = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.undo_move()

                if event.key == pygame.K_RIGHT:
                    game.redo_move()

                if event.key == pygame.K_r:
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = event.pos
                game.every_button_pressend(m_x, m_y)
                if m_x < WIDTH:
                    x, y = game.get_onclick(m_x, m_y)
                    if pygame.mouse.get_pressed()[0]:
                        game.marked_pos = [[0] * 8 for _ in range(8)]
                        if x != -1:
                            game.draw_valid_moves = True
                            selected = True
                            game.moved = False
                            game.selected_pos = (x, y)
                            game.board.board[x][y].selected = True
                            if game.turn == game.board.board[x][y].color:
                                game.get_valid_moves(x, y)

                    x, y = get_square_onclick(m_x, m_y)
                    if pygame.mouse.get_pressed()[2]:
                        if m_x < WIDTH:
                            game.mark((x, y))

            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = event.pos
                selected = False
                if m_x < WIDTH:
                    x, y = get_square_onclick(m_x, m_y)
                    if game.selected_pos:
                        game.make_move(win, game.selected_pos, (x, y))
                else:
                    if game.selected_pos:
                        print(x, y, game.selected_pos)
                        game.board.board[x][y].change_pos((x, y))


                todo_after_move()
                game.draw_window(win)

                # AI plays human

                if game.HUMAN_AI:
                    if game.moved:
                        best_move = game.minimax(win, 5, 0, 0, game.turn, WHITE)
                        if best_move:
                            game.get_valid_moves(best_move[0][0], best_move[0][1])
                            game.make_move(win, best_move[0], best_move[1])
                            todo_after_move()
                            game.moved = False

                # ...

            if event.type == pygame.MOUSEMOTION:
                m_x, m_y = event.pos
                if selected:
                    bo = game.board.board
                    if m_x > WIDTH:
                        m_x = WIDTH
                    img_x = m_x - W / 2
                    img_y = m_y - W / 2
                    for j in range(8):
                        for i in range(8):
                            if bo[i][j] != 0:
                                if bo[i][j].selected:
                                    game.board.board[i][j].x = img_x
                                    game.board.board[i][j].y = img_y

main()

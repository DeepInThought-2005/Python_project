#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 5/3/21 2:56 pm
# @Author    : Louis
# @File      : game
# @Software  : PyCharm
# Description:

from board import *
from constants import *
from piece import *
import pygame
pygame.font.init()
import random
import copy


a_cool_position = "5B1k/1R6/5p1K/1n1r3p/8/8/8/5b2 w"



class Game:
    def __init__(self):
        self.board = Board(fen="")
        self.turn = self.board.turn
        self.selected_pos = ()
        self.last_move = []
        self.started = False
        self.gameover = False
        self.en_passant_pos = ()
        self.valid_moves = []
        self.marked_pos = [[0] * 8 for _ in range(8)]
        self.undos = [] # the moves which was played
        self.redos = [] # when -> pressed, append undos.pop() to redos
        self.move_text = ""
        self.moved = False
        self.black_time = 15 * 60
        self.white_time = 15 * 60
        self.draw_valid_moves = True
        self.AI_button = [(WIDTH + 50, 150, 100, 40), "AI - AI", pygame.USEREVENT + 1]
        self.Human_Button = [(WIDTH + 50, 250, 180, 40), "HUMAN - AI", pygame.USEREVENT + 2]
        self.HUMAN_AI = False
        self.AI_AI = False


    # AI part

    def get_maxi_color(self):
        if self.turn == WHITE:
            return True
        else:
            return False

    def evaluate(self, max_color):
        self.board.get_score()
        if max_color:
            return self.board.white_score - self.board.black_score
        else:
            return self.board.black_score - self.board.white_score

    def minimax(self, win, depth, alpha, beta, maximizing_color):

        # visualization
        self.draw_window(win)

        if depth == 0 or self.board.game_over():
            return None, self.evaluate(maximizing_color)

        moves = self.board.get_valid_moves(self.turn)
        valid_moves = []
        for move in moves:
            if self.board.is_legal_move(self.turn, move[0], move[1]):
                valid_moves.append(move)

        print(valid_moves)

        best_move = random.choice(valid_moves)
        
        if maximizing_color:
            max_eval = -9999999
            for move in valid_moves:
                self.get_valid_moves(move[0][0], move[0][1])
                self.make_move(win, move[0], move[1])
                current_eval = self.minimax(win, depth - 1, alpha, beta, False)[1]
                self.undo_move()
                if current_eval > max_eval:
                    pygame.time.delay(3000)
                    max_eval = current_eval
                    print(current_eval, max_eval)
                    best_move = move

                # alpha = max(alpha, current_eval)
                # print("max: ", alpha, beta)
                # if beta <= alpha:
                #     break

            return best_move, max_eval

        else:
            min_eval = 9999999
            for move in valid_moves:
                self.get_valid_moves(move[0][0], move[0][1])
                self.make_move(win, move[0], move[1])
                current_eval = self.minimax(win, depth - 1, alpha, beta, True)[1]
                self.undo_move()
                if current_eval < min_eval:
                    pygame.time.delay(3000)
                    min_eval = current_eval
                    print(current_eval, min_eval)
                    best_move = move

                # beta = min(beta, current_eval)
                # print("min: ", alpha, beta)
                # if beta <= alpha:
                #     break
            return best_move, min_eval


    def every_button_pressend(self, m_x, m_y):
        self.button_pressed(m_x, m_y, self.AI_button)
        self.button_pressed(m_x, m_y, self.Human_Button)


    def button_pressed(self, m_x, m_y, button):
        if m_x > button[0][0] and m_x < button[0][0] + button[0][2] and \
            m_y > button[0][1] and m_y < button[0][1] + button[0][3]:
            pygame.event.post(pygame.event.Event(button[2]))


    def draw_buttons(self, win):
        pygame.draw.rect(win, WHITE, self.AI_button[0], 4)
        pygame.draw.rect(win, WHITE, self.Human_Button[0], 4)
        font = pygame.font.SysFont("Arial", 30)
        text1 = font.render(self.AI_button[1], 1, BLACK)
        text2 = font.render(self.Human_Button[1], 1, BLACK)
        win.blit(text1, (self.AI_button[0][0] + self.AI_button[0][2] / 2 - text1.get_width() / 2,
                         self.AI_button[0][1] + self.AI_button[0][3] / 2 - text1.get_height() / 2))
        win.blit(text2, (self.Human_Button[0][0] + self.Human_Button[0][2] / 2 - text2.get_width() / 2,
                         self.Human_Button[0][1] + self.Human_Button[0][3] / 2 - text2.get_height() / 2))


    def game_over(self, win, tie=False, stalemate=False):
        START_END.play()
        self.board.draw(win)
        self.board.set_every_pos()
        self.board.unselectall()
        self.board.draw_pieces(win)
        text_font = pygame.font.SysFont("times", 100)
        hint_font = pygame.font.SysFont("times", 60)
        if tie:
            text = text_font.render("Draw!", 1, red)
        elif stalemate:
            text = text_font.render(self.turn + ' stalemates!', 1, red)
        else:
            text = text_font.render(self.turn + ' checkmates!', 1, red)
        hint = hint_font.render("click anywhere to continue...", 1, red)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 4 * 3 - text.get_height() // 2))
        pygame.display.update()
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True


    def draw_color(self, win, hell_color, dark_color, pos):
        x, y = pos
        if x % 2 == 0:
            if y % 2 != 0:
                pygame.draw.rect(win, dark_color, (x * W, y * W, W, W))
            if y % 2 == 0:
                pygame.draw.rect(win, hell_color, (x * W, y * W, W, W))
        else:
            if y % 2 == 0:
                pygame.draw.rect(win, dark_color, (x * W, y * W, W, W))
            if y % 2 != 0:
                pygame.draw.rect(win, hell_color, (x * W, y * W, W, W))


    def draw_window(self, win):
        win.fill(hell_green)
        t1 = int(self.black_time)
        t2 = int(self.white_time)
        formattime1 = str(t1 // 60) + ':' + str(t1 % 60)
        formattime2 = str(t2 // 60) + ':' + str(t2 % 60)

        if t1 % 60 == 0:
            formattime1 = str(t1 // 60) + ':' + '00'
        if t2 % 60 == 0:
            formattime2 = str(t2 // 60) + ':' + '00'

        if t1 % 60 < 10:
            formattime1 = str(t1 // 60) + ':' + '0' + str(t1 % 60)
        if t2 % 60 < 10:
            formattime2 = str(t2 // 60) + ':' + '0' + str(t2 % 60)

        font1 = pygame.font.SysFont("times", 50)
        font2 = pygame.font.SysFont("Arial", 45)
        text1 = font2.render("Time: " + str(formattime1), 1, black)
        text2 = font2.render("Time: " + str(formattime2), 1, black)
        win.blit(text2, (WIDTH + 300 // 2 - text1.get_width() // 2, HEIGHT - 50 - text2.get_height() // 2))
        win.blit(text1, (WIDTH + 300 // 2 - text1.get_width() // 2, 10 + text1.get_height()))

        # draw buttons
        self.draw_buttons(win)

        move_txt = font1.render(self.move_text, 1, black)
        win.blit(move_txt, (WIDTH + 300 // 2 - move_txt.get_width() // 2, HEIGHT // 2 - move_txt.get_height() // 2))

        self.board.draw(win)

        if self.last_move:
            start = self.last_move[0]
            end = self.last_move[1]
            self.draw_color(win, hell_orange, dark_orange, start)
            self.draw_color(win, hell_orange, dark_orange, end)

        # draw valid_moves
        if self.draw_valid_moves:
            self.board.draw_valid_moves(win, self.valid_moves, self.turn)

        # draw selected
        if self.selected_pos:
            pygame.draw.rect(win, select_color, (self.selected_pos[0] * W, self.selected_pos[1] * W, W, W))

        # draw mark
        for i in range(8):
            for j in range(8):
                if self.marked_pos[i][j] == 1:
                    self.draw_color(win, hell_red, red, (i, j))

        # for check
        self.change_turn()
        king_pos = self.board.get_king_pos(self.turn)
        self.change_turn()
        m_x = pygame.mouse.get_pos()[0]
        if m_x < WIDTH:
            self.change_turn()
            if self.board.check(self.turn):
                self.change_turn()
                pygame.draw.rect(win, checked, (king_pos[0] * W, king_pos[1] * W, W, W))
            else:
                self.change_turn()

        # Draw the pieces
        self.board.draw_pieces(win)

        # solve the layer problem!
        if self.selected_pos:
            self.board.board[self.selected_pos[0]][self.selected_pos[1]].draw(win)

        pygame.display.update()

    def undo_move(self):
        if self.undos:
            bo = self.board.board
            p1, p2 = self.undos.pop()
            self.redos.append((p1, p2))
            self.board.board[p1.col][p1.row] = p1
            if isinstance(p2, tuple):
                self.last_move = [(p1.col, p1.row), (p2[0], p2[1])]
                self.board.board[p2[0]][p2[1]] = 0
            else:
                self.last_move = [(p1.col, p1.row), (p2.col, p2.row)]
                self.board.board[p2.col][p2.row] = p2

            if isinstance(p1, Pawn):
                if p1.row == 6 or p1.row == 1:
                    self.board.board[p1.col][p1.row].first = True
                if isinstance(p2, tuple) and abs(p2[0] - p1.col) == 1:
                    if p1.color == WHITE:
                        self.board.board[p2[0]][p2[1] + 1] = Pawn(p2[0], p2[1] + 1, self.board.change_turn(p1.color), 'P')
                    else:
                        self.board.board[p2[0]][p2[1] - 1] = Pawn(p2[0], p2[1] - 1, self.board.change_turn(p1.color), 'P')

            # for castles
            if isinstance(p1, King):
                if isinstance(p2, tuple):
                    if p1.color == WHITE:
                        # for castles availible
                        if abs(p1.col - p2[0]) == 2:
                            self.board.board[4][7].castled = True

                        if p1.col - p2[0] == -2:
                            self.board.board[5][7] = 0
                            self.board.board[7][7] = Rook(7, 7, p1.color, 'R')
                        elif p1.col - p2[0] == 2:
                            self.board.board[3][7] = 0
                            self.board.board[0][7] = Rook(0, 7, p1.color, 'R')
                    else:
                        # for castles availible
                        if abs(p1.col - p2[0]) == 2:
                            self.board.board[4][0].castled = True

                        if p1.col - p2[0] == -2:
                            self.board.board[5][0] = 0
                            self.board.board[7][0] = Rook(7, 0, p1.color, 'R')
                        elif p1.col - p2[0] == 2:
                            self.board.board[3][0] = 0
                            self.board.board[0][0] = Rook(0, 0, p1.color, 'R')

            self.change_turn()


    def redo_move(self):
        if self.redos:
            p1, p2 = self.redos.pop()
            self.undos.append((p1, p2))
            if isinstance(p2, tuple):
                self.last_move = [(p1.col, p1.row), (p2[0], p2[1])]
                self.board.board[p2[0]][p2[1]] = p1.__class__(p2[0], p2[1], p1.color, p1.sign)
                self.board.board[p1.col][p1.row] = 0
            else:
                self.last_move = [(p1.col, p1.row), (p2.col, p2.row)]
                self.board.board[p1.col][p1.row] = 0
                self.board.board[p2.col][p2.row] = p1.__class__(p2.col, p2.row, p1.color, p1.sign)


            if isinstance(p1, Pawn):
                if isinstance(p2, tuple):
                    self.board.board[p2[0]][p2[1]].first = False
                    if p2[1] == 7 or p2[1] == 0:
                        self.board.board[p2[0]][p2[1]].promote()
                else:
                    self.board.board[p2.col][p2.row].first = False
                    if p2.row == 7 or p2.row == 0:
                        self.board.board[p2.col][p2.row].promote()

                if isinstance(p2, tuple) and abs(p2[0] - p1.col) == 1:
                    if p1.color == WHITE:
                        self.board.board[p2[0]][p2[1] + 1] = 0
                    else:
                        self.board.board[p2[0]][p2[1] - 1] = 0

            # for castles
            if isinstance(p1, King):
                if isinstance(p2, tuple):
                    if p1.color == WHITE:
                        if p1.col - p2[0] == -2:
                            self.board.board[7][7] = 0
                            self.board.board[5][7] = Rook(5, 7, p1.color, 'R')
                        elif p1.col - p2[0] == 2:
                            self.board.board[0][7] = 0
                            self.board.board[3][7] = Rook(3, 7, p1.color, 'R')
                    else:

                        if p1.col - p2[0] == -2:
                            self.board.board[7][0] = 0
                            self.board.board[5][0] = Rook(5, 0, p1.color, 'R')
                        elif p1.col - p2[0] == 2:
                            self.board.board[0][0] = 0
                            self.board.board[3][0] = Rook(3, 0, p1.color, 'R')

            self.change_turn()


    def make_move(self, win, start, end):
        bo = self.board.board
        # self.valid_moves = self.board.get_valid_moves(self.turn)
        print("yes")
        self.board.print_board()
        if self.turn == bo[start[0]][start[1]].color:
            if start != end:
                if end in self.valid_moves:

                    if bo[end[0]][end[1]] == 0 or bo[end[0]][end[1]].color != self.turn:
                        self.moved = True
                        if bo[end[0]][end[1]] == 0:
                            MOVE.play()
                        else:
                            CAPTURE.play()

                        # the moves which can be undoed
                        s_b = self.board.board[start[0]][start[1]]
                        s_p = s_b.__class__(start[0], start[1], s_b.color, s_b.sign)
                        e_b = self.board.board[end[0]][end[1]]
                        e_p = None
                        if e_b != 0:
                            e_p = e_b.__class__(end[0], end[1], e_b.color, e_b.sign)
                        else:
                            e_p = (end[0], end[1])

                        self.undos.append((s_p, e_p))

                        self.move_text = self.board.move(start, end)
                        if not self.started:
                            START_END.play()
                        self.started = True
                        self.last_move = [start, end]

                        bo = self.board.board
                        if isinstance(bo[end[0]][end[1]], Rook):
                            self.board.board[end[0]][end[1]].castled = True

                        if isinstance(bo[end[0]][end[1]], King):
                            self.move_text = self.maybe_castles(start, end)

                        if isinstance(bo[end[0]][end[1]], Pawn):
                            if end[1] == 7 or end[1] == 0:
                                self.board.board[end[0]][end[1]].promote()
                            self.board.board[end[0]][end[1]].first = False
                            self.maybe_enpassant(start, end)

                            # set en_passant_pos
                            if abs(end[1] - start[1]) == 2:
                                self.en_passant_pos = (end[0], end[1])
                            else:
                                self.en_passant_pos = ()

                        self.change_turn()

                        print()
                        self.board.print_board()
                        print(self.move_text)
                        if self.redos:
                            if (s_p, e_p) != self.redos[-1]:
                                self.redos = []

                        # AI vs AI

                        if self.AI_AI:
                            self.draw_valid_moves = False
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    quit()

                                m_x, m_y = pygame.mouse.get_pos()
                                self.every_button_pressend(m_x, m_y)

                                if event.type == self.AI_button[2]:
                                    print("AI")
                                    if self.AI_AI:
                                        self.AI_AI = False
                                    else:
                                        self.AI_AI = True

                                if event.type == self.Human_Button[2]:
                                    print("Human")
                                    if self.HUMAN_AI:
                                        self.HUMAN_AI = False
                                    else:
                                        self.HUMAN_AI = True

                            best_move = self.minimax(win, 3, False)
                            self.get_valid_moves(best_move[0][0], best_move[0][1])
                            print(best_move)

                            self.board.set_every_pos()
                            self.selected_pos = best_move[0]
                            self.draw_window(win)
                            self.make_move(win, best_move[0], best_move[1])

                        # ...

                    elif self.board.board[end[0]][end[1]].color == self.turn:
                        self.board.board[start[0]][start[1]].change_pos((start))
                else:
                    self.board.board[start[0]][start[1]].change_pos((start))
            else:
                self.board.board[start[0]][start[1]].change_pos((start))
        else:
            if self.selected_pos:
                self.board.board[start[0]][start[1]].change_pos((start))

    def get_valid_moves(self, x, y):
        if isinstance(self.board.board[x][y], Pawn):
            valid_moves = self.board.board[x][y].get_valid_moves(self.board, en_p=self.en_passant_pos)
        else:
            valid_moves = self.board.board[x][y].get_valid_moves(self.board)
        moves = []
        for move in valid_moves:
            if self.board.is_legal_move(self.turn, (x, y), move):
                moves.append(move)
        self.valid_moves = moves


    def get_onclick(self, m_x, m_y):
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] != 0:
                    if self.board.board[i][j].onclick(m_x, m_y):
                        return i, j
        return -1, -1

    def mark(self, pos):
        x, y = pos
        if self.marked_pos[x][y] == 1:
            self.marked_pos[x][y] = 0
        else:
            self.marked_pos[x][y] = 1

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def check_gameover(self, color):
        if self.board.checkmate(color):
            return CHECKMATE
        if self.board.stalemate(color):
            return STALEMATE
        if self.board.checkdraw():
            return DRAW
        return None

    def maybe_enpassant(self, selected_pos, moved_pos):
        x, y = moved_pos
        if self.board.board[x][y].is_move_en_passant(selected_pos, self.en_passant_pos):
            if moved_pos[0] == self.en_passant_pos[0]:
                if self.turn == BLACK:
                    self.board.board[x][y - 1] = 0
                else:
                    self.board.board[x][y + 1] = 0
                CAPTURE.play()


    def maybe_castles(self, selected_pos, moved_pos):
        x, y = moved_pos
        bo = self.board.board
        move_text = ""
        if self.turn == WHITE:
            if not bo[x][y].s_castled:
                # o-o
                if bo[x][y].how_castles(selected_pos[0], selected_pos[1]) == O_O:
                    if bo[7][7] != 0:
                        if not bo[7][7].castled:
                            move_text = self.board.move((7, 7), (5, 7), castles=O_O)
                            self.board.board[x][y].s_castled = True
                            self.board.board[5][7].castled = True

            if not bo[x][y].l_castled:
                # o-o-o
                if bo[x][y].how_castles(selected_pos[0], selected_pos[1]) == O_O_O:
                    if bo[0][7] != 0:
                        if not bo[0][7].castled:
                            move_text = self.board.move((0, 7), (3, 7), castles=O_O_O)
                            self.board.board[x][y].l_castled = True
                            self.board.board[3][7].castled = True

        else:
            if not bo[x][y].s_castled:
                # o-o
                if bo[x][y].how_castles(selected_pos[0], selected_pos[1]) == O_O:
                    if bo[7][0] != 0:
                        if not bo[7][0].castled:
                            move_text = self.board.move((7, 0), (5, 0), castles=O_O)
                            self.board.board[x][y].s_castled = True
                            self.board.board[5][0].castled = True

            if not bo[x][y].s_castled:
                # o-o-o
                if bo[x][y].how_castles(selected_pos[0], selected_pos[1]) == O_O_O:
                    if bo[0][0] != 0:
                        if not bo[0][0].castled:
                            move_text = self.board.move((0, 0), (3, 0), castles=O_O_O)
                            self.board.board[x][y].l_castled = True
                            self.board.board[3][0].castled = True

        return move_text










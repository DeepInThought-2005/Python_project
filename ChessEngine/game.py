#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 5/3/21 2:56 pm
# @Author    : Louis
# @File      : game
# @Software  : PyCharm
# Description:

from board import *
from constants import *
import pygame



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


    def draw_window(self, win, black_time, white_time):
        win.fill(hell_green)
        t1 = black_time
        t2 = white_time
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

        move_txt = font1.render(self.move_text, 1, black)
        win.blit(move_txt, (WIDTH + 300 // 2 - move_txt.get_width() // 2, HEIGHT // 2 - move_txt.get_height() // 2))

        self.board.draw(win)

        if self.last_move:
            start = self.last_move[0]
            end = self.last_move[1]
            self.draw_color(win, hell_orange, dark_orange, start)
            self.draw_color(win, hell_orange, dark_orange, end)

        self.board.draw_valid_moves(win, self.valid_moves, self.turn)

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
            print((p1.col, p1.row), p2)
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

            self.change_turn()


    def redo_move(self):
        if self.redos:
            p1, p2 = self.redos.pop()
            self.undos.append((p1, p2))
            print(p1, p2)
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
                    if p2[0] == 7 or p2[1] == 0:
                        self.board.board[p2[0]][p2[1]].promote()
                else:
                    if p2.row == 7 or p2.row == 0:
                        self.board.board[p2.col][p2.row].promote()

            self.change_turn()


    def make_move(self, win, start, end):
        bo = self.board.board
        # self.valid_moves = self.board.get_valid_moves(self.turn)
        if self.turn == bo[start[0]][start[1]].color:
            if start != end:
                if end in self.valid_moves:
                    if bo[end[0]][end[1]] == 0 or bo[end[0]][end[1]].color != self.turn:
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

                        # check game result
                        result = self.check_gameover(self.turn)
                        if result == CHECKMATE:
                            self.game_over(win)
                            self.gameover = True
                        elif result == STALEMATE:
                            self.game_over(win, stalemate=True)
                            self.gameover = True
                        elif result == DRAW:
                            self.game_over(win, tie=True)
                            self.gameover = True

                        self.change_turn()

                        print()
                        self.board.print_board()
                        print(self.move_text)
                        if self.redos:
                            if (s_p, e_p) != self.redos[-1]:
                                self.redos = []


                    elif self.board.board[end[0]][end[1]].color == self.turn:
                        self.board.board[start[0]][start[1]].change_pos((start))
                else:
                    self.board.board[start[0]][start[1]].change_pos((start))
            else:
                self.board.board[start[0]][start[1]].change_pos((start))
        else:
            if self.selected_pos:
                self.board.board[start[0]][start[1]].change_pos((start))


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










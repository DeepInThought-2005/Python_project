import pygame
from piece import *
from constants import *


class Board:
    piece_values = {"Q": 900,
                    "K": 0,
                    "B": 300,
                    "N": 300,
                    "R": 500,
                    "P": 100}

    def __init__(self, fen=""):
        self.board = [[0] * 8 for _ in range(8)]
        self.turn = WHITE
        self.img = BOARD
        self.img = pygame.image.load(self.img)
        self.img = pygame.transform.scale(self.img, (WIDTH, WIDTH))
        if fen:
            self.load_FEN(fen)
        else:
            self.generate_board()

    def game_over(self):
        pass

    def get_score(self):
        self.white_score = 0
        self.black_score = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color == WHITE:
                    self.white_score += self.piece_values[self.board[i][j].sign]
                else:
                    self.white_score += self.piece_values[self.board[i][j].sign]

    def load_FEN(self, fen):
        fen = fen.replace(' ', '')
        self.board = [[0] * 8 for _ in range(8)]
        i = -1
        j = 0
        for k, x in enumerate(fen):
            if x == 'Q':
                i += 1
                self.board[i][j] = Queen(i, j, WHITE, "Q")
            elif x == 'K':
                i += 1
                self.board[i][j] = King(i, j, WHITE, "K")
            elif x == 'B':
                i += 1
                self.board[i][j] = Bishop(i, j, WHITE, "B")
            elif x == 'N':
                i += 1
                self.board[i][j] = Knight(i, j, WHITE, "N")
            elif x == 'R':
                i += 1
                self.board[i][j] = Rook(i, j, WHITE, "R")
            elif x == 'P':
                i += 1
                self.board[i][j] = Pawn(i, j, WHITE, "P")
            elif x == 'q':
                i += 1
                self.board[i][j] = Queen(i, j, BLACK, "Q")
            elif x == 'k':
                i += 1
                self.board[i][j] = King(i, j, BLACK, "K")
            elif x == 'b':
                i += 1
                self.board[i][j] = Bishop(i, j, BLACK, "B")
            elif x == 'n':
                i += 1
                self.board[i][j] = Knight(i, j, BLACK, "N")
            elif x == 'r':
                i += 1
                self.board[i][j] = Rook(i, j, BLACK, "R")
            elif x == 'p':
                i += 1
                self.board[i][j] = Pawn(i, j, BLACK, "P")
            elif x == '/':
                j += 1
                i = -1
            else:
                i += int(x)

            if i == 7 and j == 7:
                if fen[k + 1] == 'b':
                    self.turn = BLACK
                else:
                    self.turn = WHITE
                break



    # def flip(self):
    #     tboard = self.board[:]
    #     for i in range(8):
    #         tboard.append([])
    #         for j in range(8):
    #             tboard[i].append(self.board[i][7 - j])
    #             if self.board[i][7 - j] != 0 and self.board[i][j] != 0:
    #                 self.board[i][j].col, self.board[i][j].row, self.board[i][7 - j].col, self.board[i][7 - j].row = \
    #                 i, 7 - j, i, j
    #             if self.board[i][7 - j] == 0 and self.board[i][j] != 0:
    #                 self.board[i][j].change_pos((i, 7 - j))
    #             elif self.board[i][7 - j] != 0 and self.board[i][j] == 0:
    #                 self.board[i][7 - j].change_pos((i, j))

    #     self.board = tboard
    #     self.set_every_pos()


    def change_turn(self, turn):
        if turn == BLACK:
            turn = WHITE
        else:
            turn = BLACK
        return turn

    def checkdraw(self):
        count = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if not isinstance(self.board[i][j], King):
                        count += 1

        if not count:
            return True

        if count <= 4:
            b_n = b_b = w_n = w_b = 0
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != 0:
                        if self.board[i][j].color == WHITE:
                            if isinstance(self.board[i][j], Knight):
                                w_n += 1
                            if isinstance(self.board[i][j], Bishop):
                                w_b += 1
                        else:
                            if isinstance(self.board[i][j], Knight):
                                b_n += 1
                            if isinstance(self.board[i][j], Bishop):
                                b_b += 1
            if count == 1:
                if b_n == 1 or b_b == 1 or w_n == 1 or w_b == 1:
                    return True

            elif count == 2:
                if b_n == 1 and w_n == 1 or \
                   b_n == 1 and w_b == 1 or \
                   b_b == 1 and w_n == 1 or \
                   b_b == 1 and w_b == 1:
                    return True

                if b_n == 2 or w_n == 2:
                    return True

            elif count == 3:
                if w_n == 2 and b_n == 1 or w_n == 2 and b_b == 1 or \
                   b_n == 2 and w_n == 1 or b_n == 2 and w_b == 1:
                    return True

            else:
                if w_n == 2 and b_n == 2:
                    return True

        return False


    def checkmate(self, turn):
        danger_moves = self.get_danger_moves(turn)
        checkers = self.get_checkers(turn)
        defend_moves = self.get_danger_moves(self.change_turn(turn), for_checkmate=True)
        # print(defend_moves)
        valid_king_moves = []
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], King):
                    if turn != self.board[i][j].color:
                        for move in self.board[i][j].get_valid_moves(self):
                            valid_king_moves.append(move)

        if self.check(turn):
            for move in valid_king_moves:
                if move not in danger_moves:
                    return False

            for checker in checkers:
                for move in defend_moves:
                    if move in self.board[checker[0]][checker[1]].get_danger_moves(self):
                        if checker not in valid_king_moves:
                            return False

                if checker in defend_moves:
                    return False

            return True

    def check(self, turn):
        danger_moves = self.get_danger_moves(turn)
        king_pos = self.get_king_pos(turn)

        if king_pos in danger_moves:
            return True

        return False


    def get_checkers(self, turn):
        king_pos = self.get_king_pos(turn)

        checkers = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == turn:
                        if king_pos in self.board[i][j].get_danger_moves(self):
                            checkers.append((i, j))

        return checkers

    def draw(self, win):
        win.blit(self.img, (0, 0))
        # for i in range(8):
        #     for j in range(8):
        #         color = ()
        #         if i % 2 == 0:
        #             if j % 2 != 0:
        #                 color = green
        #             if j % 2 == 0:
        #                 color = white
        #         else:
        #             if j % 2 == 0:
        #                 color = green
        #             if j % 2 != 0:
        #                 color = white
        #
        #         pygame.draw.rect(win, color, (j * W, i * W, W, W))

    def get_king_pos(self, turn):
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], King):
                    if turn != self.board[i][j].color:
                        king_pos = (i, j)
                        return king_pos


    def generate_board(self):
        # generate white pieces
        self.board[0][7] = Rook  (0, 7, WHITE, 'R')
        self.board[1][7] = Knight(1, 7, WHITE, 'N')
        self.board[2][7] = Bishop(2, 7, WHITE, 'B')
        self.board[3][7] = Queen (3, 7, WHITE, 'Q')
        self.board[4][7] = King  (4, 7, WHITE, 'K')
        self.board[5][7] = Bishop(5, 7, WHITE, 'B')
        self.board[6][7] = Knight(6, 7, WHITE, 'N')
        self.board[7][7] = Rook  (7, 7, WHITE, 'R')
        for i in range(8):
            self.board[i][6] = Pawn(i, 6, WHITE, 'P')

        # generate black pieces
        self.board[0][0] = Rook  (0, 0, BLACK, 'R')
        self.board[1][0] = Knight(1, 0, BLACK, 'N')
        self.board[2][0] = Bishop(2, 0, BLACK, 'B')
        self.board[3][0] = Queen (3, 0, BLACK, 'Q')
        self.board[4][0] = King  (4, 0, BLACK, 'K')
        self.board[5][0] = Bishop(5, 0, BLACK, 'B')
        self.board[6][0] = Knight(6, 0, BLACK, 'N')
        self.board[7][0] = Rook  (7, 0, BLACK, 'R')
        for i in range(8):
            self.board[i][1] = Pawn(i, 1, BLACK, 'P')

    def get_danger_moves(self, turn, for_checkmate=False):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == turn:
                        if for_checkmate:
                            if isinstance(self.board[i][j], Pawn):
                                for move in self.board[i][j].get_valid_moves(self):
                                    moves.append(move)
                            else:
                                if not isinstance(self.board[i][j], King):
                                    for move in self.board[i][j].get_danger_moves(self):
                                        moves.append(move)

                        if not for_checkmate:
                            for move in self.board[i][j].get_danger_moves(self):
                                moves.append(move)


        return moves

    def print_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    font_color = ''
                    if self.board[j][i].color == WHITE:
                        font_color = '37m'
                    else:
                        font_color = '31m'
                    print("\033[1;" + font_color + self.board[j][i].sign + "\033[0m", end=' ')
                else:
                    print('.', end=' ')
            print()

    def move(self, pos1, pos2, castles=""):
        tboard = self.board[:]
        tboard[pos1[0]][pos1[1]].change_pos(pos2)
        self.board[pos2[0]][pos2[1]], self.board[pos1[0]][pos1[1]] = self.board[pos1[0]][pos1[1]], 0
        self.board = tboard
        self.set_every_pos()
        if castles == O_O:
            return O_O
        elif castles == O_O_O:
            return O_O_O
        else:
            return chr(ord('a') + pos1[0]) + str(8 - pos1[1]) + chr(ord('a') + pos2[0]) + str(8 - pos2[1])

    def set_every_pos(self):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    self.board[j][i].set_pos()

    def set_every_coord(self):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    self.board[j][i].set_coord()

    def unselectall(self):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    self.board[j][i].selected = False

    def is_legal_move(self, turn, start, end):
        tboard = Board()
        tboard.board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                tboard.board[i][j] = self.board[i][j]
        tboard.move(start, end)
        turn = self.change_turn(turn)
        if tboard.check(turn):
            tboard.move(end, start)
            return False
        tboard.move(end, start)
        return True            

    def draw_valid_moves(self, win, moves, board, turn):
        if moves:
            for move in moves:
                if board[move[0]][move[1]] == 0:
                    pygame.draw.circle(win, hell_gray, (move[0] * W + W // 2, move[1] * W + W // 2), W // 5)
                else:
                    if turn != board[move[0]][move[1]].color:
                        pygame.draw.circle(win, hell_gray, (move[0] * W + W // 2, move[1] * W + W // 2), W // 2, 8)



import asyncio
import pygame
from constants import *

PROMOTION_IMAGES = {
    WHITE: {"Q": WHITE_QUEEN, "R": WHITE_ROOK, "B": WHITE_BISHOP, "N": WHITE_KNIGHT},
    BLACK: {"Q": BLACK_QUEEN, "R": BLACK_ROOK, "B": BLACK_BISHOP, "N": BLACK_KNIGHT},
}

class Piece:
    def __init__(self, col, row, color, sign):
        self.w = 100
        self.h = 100
        self.img_type = ''
        if color == BLACK:
            if sign == 'R':
                self.img_type = BLACK_ROOK
            elif sign == 'N':
                self.img_type = BLACK_KNIGHT
            elif sign == 'B':
                self.img_type = BLACK_BISHOP
            elif sign == 'K':
                self.img_type = BLACK_KING
            elif sign == 'Q':
                self.img_type = BLACK_QUEEN
            elif sign == 'P':
                self.img_type = BLACK_PAWN

        else:
            if sign == 'R':
                self.img_type = WHITE_ROOK
            elif sign == 'N':
                self.img_type = WHITE_KNIGHT
            elif sign == 'B':
                self.img_type = WHITE_BISHOP
            elif sign == 'K':
                self.img_type = WHITE_KING
            elif sign == 'Q':
                self.img_type = WHITE_QUEEN
            elif sign == 'P':
                self.img_type = WHITE_PAWN

        self.img = load_image(self.img_type, (self.w, self.h))

        self.sign = sign
        self.col = col
        self.row = row
        self.x = self.col * self.w
        self.y = self.row * self.h
        self.set_pos()
        self.color = color
        self.selected = False

    def resize(self, w, h):
        self.w = w // 8
        self.h = h // 8
        self.img = load_image(self.img_type, (w // 8, h // 8))
        # self.set_pos()

    def change_turn(self, turn):
        if turn == BLACK:
            turn = WHITE
        else:
            turn = BLACK
        return turn

    def change_pos(self, end):
        self.col = end[0]
        self.row = end[1]
        return self.col, self.row

    def set_coord(self):
        if self.w != 0 and self.h != 0:
            self.col = round(self.x / self.w)
            self.row = round(self.y / self.h)
            self.pos = (self.col, self.row)

    def set_pos(self):
        self.x = self.col * self.w
        self.y = self.row * self.h

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def onclick(self, m_x, m_y):
        if m_x >= self.x and m_x <= self.x + self.w and m_y >= self.y and m_y <= self.y + self.h:
            return True
        return False

    def __str__(self):
        return str(self.sign + str(self.col) + str(self.row))


class Queen(Piece):
    def __init__(self, col, row, color, sign):
        super().__init__(col, row, color, sign)
        self.value = 900

    def get_danger_moves(self, board):
        board = board.board
        moves = []
        i = self.col
        j = self.row

        diL, diR = i + 1, i - 1
        # UP RIGHT
        for dj in range(j - 1, -1, -1):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                else:
                    moves.append((diL, dj))
                    break
            else:
                break
            diL += 1

        # UP LEFT
        for dj in range(j - 1, -1, -1):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                else:
                    moves.append((diR, dj))
                    break
            else:
                break
            diR -= 1

        # DOWN RIGHT
        diL, diR = i + 1, i - 1
        for dj in range(j + 1, 8):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                else:
                    moves.append((diL, dj))
                    break
                diL += 1

        # DOWN LEFT
        for dj in range(j + 1, 8):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                else:
                    moves.append((diR, dj))
                    break
                    
                diR -= 1

        i, j = self.col, self.row
        # UP
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            else:
                moves.append((i, x))
                break

        #DOWN
        for x in range(j + 1, 8):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            else:
                moves.append((i, x))
                break

        #LEFT
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            else:
                moves.append((x, j))
                break

        #RIGHT
        for x in range(i + 1, 8):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            else:
                moves.append((x, j))
                break

        return moves



    def get_valid_moves(self, board):
        board = board.board
        moves = []
        i = self.col
        j = self.row

        diL, diR = i + 1, i - 1
        # UP RIGHT
        for dj in range(j - 1, -1, -1):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                elif p.color != self.color:
                    moves.append((diL, dj))
                    break
                else:
                    break
            else:
                break
            diL += 1

        # UP LEFT
        for dj in range(j - 1, -1, -1):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                elif p.color != self.color:
                    moves.append((diR, dj))
                    break
                else:
                    break
            else:
                break
            diR -= 1

        # DOWN RIGHT
        diL, diR = i + 1, i - 1
        for dj in range(j + 1, 8):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                elif p.color != self.color:
                    moves.append((diL, dj))
                    break
                else:
                    break
                diL += 1

        # DOWN LEFT
        for dj in range(j + 1, 8):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                elif p.color != self.color:
                    moves.append((diR, dj))
                    break
                else:
                    break
                    
                diR -= 1

        i, j = self.col, self.row
        # UP
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            elif p.color != self.color:
                moves.append((i, x))
                break
            else:
                break

        #DOWN
        for x in range(j + 1, 8):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            elif p.color != self.color:
                moves.append((i, x))
                break
            else:
                break

        #LEFT
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            elif p.color != self.color:
                moves.append((x, j))
                break
            else:
                break

        #RIGHT
        for x in range(i + 1, 8):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            elif p.color != self.color:
                moves.append((x, j))
                break
            else:
                break

        return moves

class King(Piece):
    def __init__(self, col, row, color, sign):
        super().__init__(col, row, color, sign)
        self.s_castled = False # o-o
        self.l_castled = False # o-o-o
        self.castled = False
        self.value = 0

    def how_castles(self, x, y):
        print(self.col, x)
        result = ""
        if self.row == y:
            if self.col - x > 1:
                result = O_O
            elif self.col - x < -1:
                result = O_O_O
        return result


    def get_danger_moves(self, board):
        board = board.board
        i = self.col
        j = self.row

        moves = []

        if j > 0:
            # TOP LEFT
            if i > 0:
                p = board[i - 1][j - 1]
                moves.append((i - 1, j - 1))

            # TOP MIDDLE
            p = board[i][j - 1]
            moves.append((i, j - 1))

            # TOP RIGHT
            if i < 7:
                p = board[i + 1][j - 1]
                moves.append((i + 1, j - 1))

        if j < 7:
            # BOTTOM LEFT
            if i > 0:
                p = board[i - 1][j + 1]
                moves.append((i - 1, j + 1))

            # BOTTOM MODDLE
            p = board[i][j + 1]
            moves.append((i, j + 1))

            # BOTTOM RIGHT
            if i < 7:
                p = board[i + 1][j + 1]
                moves.append((i + 1, j + 1))

        # LEFT
        if i > 0:
            p = board[i - 1][j]
            moves.append((i - 1, j))

        # RIGHT
        if i < 7:
            p = board[i + 1][j]
            moves.append((i + 1, j))

        return moves

    def get_valid_moves(self, board):
        tboard = board.board
        i = self.col
        j = self.row

        moves = []

        if j > 0:
            # TOP LEFT
            if i > 0:
                p = tboard[i - 1][j - 1]
                if p == 0 or p.color != self.color:
                    moves.append((i - 1, j - 1))

            # TOP MIDDLE
            p = tboard[i][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((i, j - 1))

            # TOP RIGHT
            if i < 7:
                p = tboard[i + 1][j - 1]
                if p == 0 or p.color != self.color:
                    moves.append((i + 1, j - 1))

        if j < 7:
            # BOTTOM LEFT
            if i > 0:
                p = tboard[i - 1][j + 1]
                if p == 0 or p.color != self.color:
                    moves.append((i - 1, j + 1))

            # BOTTOM MODDLE
            p = tboard[i][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((i, j + 1))

            # BOTTOM RIGHT
            if i < 7:
                p = tboard[i + 1][j + 1]
                if p == 0 or p.color != self.color:
                    moves.append((i + 1, j + 1))

        # LEFT
        if i > 0:
            p = tboard[i - 1][j]
            if p == 0 or p.color != self.color:
                moves.append((i - 1, j))

        # RIGHT
        if i < 7:
            p = tboard[i + 1][j]
            if p == 0 or p.color != self.color:
                moves.append((i + 1, j))

        # CASTLES
        if not self.castled:
            if self.color == BLACK:
                if not board.check(self.change_turn(self.color)):
                    if not self.s_castled:
                        if isinstance(tboard[7][0], Rook):
                            if not tboard[7][0].castled and tboard[7][0].color == self.color:
                                if tboard[5][0] == 0 and tboard[6][0] == 0 and not tboard[7][0].castled:
                                    moves.append((5, 0))
                                    moves.append((6, 0))
                    if not self.l_castled:
                        if isinstance(tboard[0][0], Rook):
                            if not tboard[0][0].castled and tboard[0][0].color == self.color:
                                if tboard[1][0] == 0 and tboard[2][0] == 0 and tboard[3][0] == 0 and not tboard[0][0].castled:
                                    moves.append((2, 0))
                                    moves.append((3, 0))
            else:
                if not board.check(self.change_turn(self.color)):
                    if not self.s_castled:
                        if isinstance(tboard[7][7], Rook):
                            if not tboard[7][7].castled and tboard[7][7].color == self.color:
                                if tboard[5][7] == 0 and tboard[6][7] == 0 and not tboard[7][7].castled:
                                    moves.append((5, 7))
                                    moves.append((6, 7))
                    if not self.l_castled:
                        if isinstance(tboard[0][7], Rook):
                            if not tboard[0][7].castled and tboard[0][7].color == self.color:
                                if tboard[1][7] == 0 and tboard[2][7] == 0 and tboard[3][7] == 0 and not tboard[0][7].castled:
                                    moves.append((2, 7))
                                    moves.append((3, 7))
        return moves


class Bishop(Piece):
    def __init__(self, col, row, color, sign):
        super().__init__(col, row, color, sign)
        self.value = 300

    def get_danger_moves(self, board):
        board = board.board
        moves = []
        i = self.col
        j = self.row

        diL, diR = i + 1, i - 1
        # UP RIGHT
        for dj in range(j - 1, -1, -1):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                else:
                    moves.append((diL, dj))
                    break
            else:
                break
            diL += 1

        # UP LEFT
        for dj in range(j - 1, -1, -1):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                else:
                    moves.append((diR, dj))
                    break
            else:
                break
            diR -= 1

        # DOWN RIGHT
        diL, diR = i + 1, i - 1
        for dj in range(j + 1, 8):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                else:
                    moves.append((diL, dj))
                    break
                diL += 1

        # DOWN LEFT
        for dj in range(j + 1, 8):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                else:
                    moves.append((diR, dj))
                    break
                    
                diR -= 1

        return moves

    def get_valid_moves(self, board):
        board = board.board
        moves = []
        i = self.col
        j = self.row

        diL, diR = i + 1, i - 1
        # UP RIGHT
        for dj in range(j - 1, -1, -1):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                elif p.color != self.color:
                    moves.append((diL, dj))
                    break
                else:
                    break
            else:
                break
            diL += 1

        # UP LEFT
        for dj in range(j - 1, -1, -1):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                elif p.color != self.color:
                    moves.append((diR, dj))
                    break
                else:
                    break
            else:
                break
            diR -= 1

        # DOWN RIGHT
        diL, diR = i + 1, i - 1
        for dj in range(j + 1, 8):
            if diL < 8:
                p = board[diL][dj]
                if p == 0:
                    moves.append((diL, dj))
                elif p.color != self.color:
                    moves.append((diL, dj))
                    break
                else:
                    break
                diL += 1

        # DOWN LEFT
        for dj in range(j + 1, 8):
            if diR > -1:
                p = board[diR][dj]
                if p == 0:
                    moves.append((diR, dj))
                elif p.color != self.color:
                    moves.append((diR, dj))
                    break
                else:
                    break
                    
                diR -= 1

        return moves

class Knight(Piece):
    def __init__(self, col, row, color, sign):
        super().__init__(col, row, color, sign)
        self.value = 300

    def get_danger_moves(self, board):
        board = board.board
        i = self.col
        j = self.row

        moves = []

        # DOWN LEFT
        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            moves.append((i - 1, j + 2))

        # UP LEFT
        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            moves.append((i - 1, j - 2))

        # DOWN RIGHT
        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            moves.append((i + 1, j + 2))

        # UP RIGHT
        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            moves.append((i + 1, j - 2))

        # MIDDLE UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            moves.append((i - 2, j - 1))

        # MIDDLE DOWN LEFT
        if i > 1 and j < 7:
            p = board[i - 2][j + 1]
            moves.append((i - 2, j + 1))

        # MIDDLE UP RIGHT
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            moves.append((i + 2, j - 1))

        # MIDDLE DOWN RIGHT
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            moves.append((i + 2, j + 1))

        return moves


    def get_valid_moves(self, board):
        board = board.board
        i = self.col
        j = self.row

        moves = []

        # DOWN LEFT
        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p == 0 or p.color != self.color:
                moves.append((i - 1, j + 2))

        # UP LEFT
        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == 0 or p.color != self.color:
                moves.append((i - 1, j - 2))

        # DOWN RIGHT
        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p == 0 or p.color != self.color:
                moves.append((i + 1, j + 2))

        # UP RIGHT
        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p == 0 or p.color != self.color:
                moves.append((i + 1, j - 2))

        # MIDDLE UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((i - 2, j - 1))

        # MIDDLE DOWN LEFT
        if i > 1 and j < 7:
            p = board[i - 2][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((i - 2, j + 1))

        # MIDDLE UP RIGHT
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((i + 2, j - 1))

        # MIDDLE DOWN RIGHT
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((i + 2, j + 1))

        return moves

class Rook(Piece):
    def __init__(self, col, row, color, sign):
        super().__init__(col, row, color, sign)
        self.castled = False
        self.value = 500

    def get_danger_moves(self, board):
        board = board.board
        moves = []
        i, j = self.col, self.row
        # UP
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            else:
                moves.append((i, x))
                break

        #DOWN
        for x in range(j + 1, 8):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            else:
                moves.append((i, x))
                break

        #LEFT
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            else:
                moves.append((x, j))
                break

        #RIGHT
        for x in range(i + 1, 8):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            else:
                moves.append((x, j))
                break

        return moves

    def get_valid_moves(self, board):
        board = board.board
        moves = []
        i, j = self.col, self.row
        # UP
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            elif p.color != self.color:
                moves.append((i, x))
                break
            else:
                break

        #DOWN
        for x in range(j + 1, 8):
            p = board[i][x]
            if p == 0:
                moves.append((i, x))
            elif p.color != self.color:
                moves.append((i, x))
                break
            else:
                break

        #LEFT
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            elif p.color != self.color:
                moves.append((x, j))
                break
            else:
                break

        #RIGHT
        for x in range(i + 1, 8):
            p = board[x][j]
            if p == 0:
                moves.append((x, j))
            elif p.color != self.color:
                moves.append((x, j))
                break
            else:
                break

        return moves

class Pawn(Piece):
    def __init__(self, col, row, color, sign):
        super().__init__(col, row, color, sign)
        self.first = True
        self.pawn = True
        self.promoted = False
        self.value = 100

    def is_move_en_passant(self, pos, en_p=()):
        i, j = self.col, self.row
        print(j)
        if en_p:
            print(pos, en_p)
            if self.color == BLACK:
                if pos[1] == en_p[1] and pos[1] + 1 == 5:
                    return True
            else:
                if pos[1] == en_p[1] and pos[1] - 1 == 2:
                    return True
            return False

    async def promote(self, x, y, choice=None):
        # (x, y) is where the pawn came from. Without a choice, the player picks a
        # piece from a column drawn over the board; clicking elsewhere cancels the move.
        if choice is None:
            choice = await self.choose_promotion()
        if choice is None:
            self.col, self.row = x, y
            self.set_pos()
            return
        self.sign = choice
        self.img_type = PROMOTION_IMAGES[self.color][choice]
        self.img = load_image(self.img_type, (self.w, self.h))
        self.promoted = True

    async def choose_promotion(self):
        win = pygame.display.get_surface()
        w, h = win.get_width() // 8, win.get_height() // 8
        step = 1 if self.row == 0 else -1
        options = [(sign, (self.col, self.row + i * step)) for i, sign in enumerate("QRBN")]
        shade = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 120))
        win.blit(shade, (0, 0))
        for sign, (c, r) in options:
            pygame.draw.rect(win, (245, 245, 245), (c * w, r * h, w, h))
            pygame.draw.rect(win, (60, 60, 60), (c * w, r * h, w, h), 2)
            win.blit(load_image(PROMOTION_IMAGES[self.color][sign], (w, h)), (c * w, r * h))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    c, r = event.pos[0] // w, event.pos[1] // h
                    for sign, square in options:
                        if square == (c, r):
                            return sign
                    return None
            await asyncio.sleep(0)
    
        
    
    def get_danger_moves(self, board, en_p=()):
        tboard = board.board
        moves = []
        i, j = self.col, self.row
        if not self.promoted:
            if self.color == BLACK:
                if en_p:
                    if j == en_p[1]:
                        moves.append((en_p[0], j + 1))
                if j + 1 < 8:
                    if i + 1 < 8:
                        # if tboard[i + 1][j + 1] != 0:
                            moves.append((i + 1, j + 1))

                    if i - 1 > -1:
                        # if tboard[i - 1][j + 1] != 0:
                            moves.append((i - 1, j + 1))

            else:
                if en_p:
                    if j == en_p[1]:
                        moves.append((en_p[0], j - 1))
                if i + 1 < 8:
                    # if tboard[i + 1][j - 1] != 0:
                        moves.append((i + 1, j - 1))
                if i - 1 > -1:
                    # if tboard[i - 1][j - 1] != 0:
                        moves.append((i - 1, j - 1))
        else:
            if self.sign == "Q":
                queen = Queen(self.col, self.row, self.color, 'Q')
                moves = queen.get_danger_moves(board)
            elif self.sign == "R":
                rook = Rook(self.col, self.row, self.color, 'R')
                moves = rook.get_danger_moves(board)
            elif self.sign == "B":
                bishop = Bishop(self.col, self.row, self.color, 'B')
                moves = bishop.get_danger_moves(board)
            elif self.sign == "N":
                knight = Knight(self.col, self.row, self.color, 'N')
                moves = knight.get_danger_moves(board)
        return moves


    def get_valid_moves(self, board, en_p=()):
        tboard = board.board
        moves = []
        i, j = self.col, self.row
        if not self.promoted:
            if self.color == BLACK:
                if en_p:
                    if j == en_p[1]:
                        moves.append((en_p[0], j + 1))
                if j + 1 <= 7:
                    if i + 1 <= 7:
                        if tboard[i + 1][j + 1] != 0:
                            if tboard[i + 1][j + 1].color != self.color:
                                moves.append((i + 1, j + 1))

                    if i - 1 >= 0:
                        if tboard[i - 1][j + 1] != 0:
                            if tboard[i - 1][j + 1].color != self.color:
                                moves.append((i - 1, j + 1))


                    if self.first:
                        if tboard[i][j + 1] == 0:
                            moves.append((i, j + 1))
                            if tboard[i][j + 2] == 0:
                                moves.append((i, j + 2))
                    else:
                        if tboard[i][j + 1] == 0:
                                moves.append((i, j + 1))

            else:
                if en_p:
                    if j == en_p[1] and abs(i - en_p[0]) == 1:
                        moves.append((en_p[0], j - 1))
                if i + 1 <= 7:
                    if tboard[i + 1][j - 1] != 0:
                        if tboard[i + 1][j - 1].color != self.color:
                            moves.append((i + 1, j - 1))
                if i - 1 >= 0:
                    if tboard[i - 1][j - 1] != 0:
                        if tboard[i - 1][j - 1].color != self.color:
                            moves.append((i - 1, j - 1))
                if self.first:
                    if tboard[i][j - 1] == 0:
                        moves.append((i, j - 1))
                        if tboard[i][j - 2] == 0:
                            moves.append((i, j - 2))
                else:
                    if tboard[i][j - 1] == 0:
                        moves.append((i, j - 1))
        else:
            if self.sign == "Q":
                queen = Queen(self.col, self.row, self.color, 'Q')
                moves = queen.get_valid_moves(board)
            elif self.sign == "R":
                rook = Rook(self.col, self.row, self.color, 'R')
                moves = rook.get_valid_moves(board)
            elif self.sign == "B":
                bishop = Bishop(self.col, self.row, self.color, 'B')
                moves = bishop.get_valid_moves(board)
            elif self.sign == "N":
                knight = Knight(self.col, self.row, self.color, 'N')
                moves = knight.get_valid_moves(board)

        return moves





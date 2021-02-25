import pygame
from constants import *

class Piece:
    def __init__(self, col, row, color, sign):
        if color == BLACK:
            if sign == 'R':
                self.img = BLACK_ROOK
            elif sign == 'N':
                self.img = BLACK_KNIGHT
            elif sign == 'B':
                self.img = BLACK_BISHOP
            elif sign == 'K':
                self.img = BLACK_KING
            elif sign == 'Q':
                self.img = BLACK_QUEEN
            elif sign == 'P':
                self.img = BLACK_PAWN

        else:
            if sign == 'R':
                self.img = WHITE_ROOK
            elif sign == 'N':
                self.img = WHITE_KNIGHT
            elif sign == 'B':
                self.img = WHITE_BISHOP
            elif sign == 'K':
                self.img = WHITE_KING
            elif sign == 'Q':
                self.img = WHITE_QUEEN
            elif sign == 'P':
                self.img = WHITE_PAWN

        self.img = pygame.image.load(self.img)
        self.img = pygame.transform.scale(self.img, (W, W))

        self.sign = sign
        self.col = col
        self.row = row
        self.x = self.col * W
        self.y = self.row * W
        self.set_pos()
        self.color = color
        self.selected = False

    def change_pos(self, end):
        self.col = end[0]
        self.row = end[1]
        return self.col, self.row

    def set_coord(self):
        self.col = round(self.x / W)
        self.row = round(self.y / W)
        self.pos = (self.col, self.row)

    def set_pos(self):
        self.x = self.col * W
        self.y = self.row * W

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        self.set_coord()

    def onclick(self, m_x, m_y):
        if m_x > self.x and m_x < self.x + W and m_y > self.y and m_y < self.y + W:
            return True
        return False

    def __str__(self):
        return self.sign


class Queen(Piece):

    def get_danger_moves(self, board):
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
        self.castled = False

    def is_move_castle(self, x, y):
        print(self.col, x, self.row, y)
        result = None
        if self.row == y:
            if self.col - x > 0:
                result = O_O
            if self.col - x < 0:
                result = O_O_O

        return result


    def get_danger_moves(self, board):
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
        i = self.col
        j = self.row

        moves = []

        if j > 0:
            # TOP LEFT
            if i > 0:
                p = board[i - 1][j - 1]
                if p == 0 or p.color != self.color:
                    moves.append((i - 1, j - 1))

            # TOP MIDDLE
            p = board[i][j - 1]
            if p == 0 or p.color != self.color:
                moves.append((i, j - 1))

            # TOP RIGHT
            if i < 7:
                p = board[i + 1][j - 1]
                if p == 0 or p.color != self.color:
                    moves.append((i + 1, j - 1))

        if j < 7:
            # BOTTOM LEFT
            if i > 0:
                p = board[i - 1][j + 1]
                if p == 0 or p.color != self.color:
                    moves.append((i - 1, j + 1))

            # BOTTOM MODDLE
            p = board[i][j + 1]
            if p == 0 or p.color != self.color:
                moves.append((i, j + 1))

            # BOTTOM RIGHT
            if i < 7:
                p = board[i + 1][j + 1]
                if p == 0 or p.color != self.color:
                    moves.append((i + 1, j + 1))

        # LEFT
        if i > 0:
            p = board[i - 1][j]
            if p == 0 or p.color != self.color:
                moves.append((i - 1, j))

        # RIGHT
        if i < 7:
            p = board[i + 1][j]
            if p == 0 or p.color != self.color:
                moves.append((i + 1, j))

        # CASTLES
        if not self.castled:
            if self.color == BLACK:
                if board[7][0] != 0:
                    if board[5][0] == 0 and board[6][0] == 0 and not board[7][0].castled:
                        moves.append((5, 0))
                        moves.append((6, 0))
                if board[0][0] != 0:
                    if board[1][0] == 0 and board[2][0] == 0 and board[3][0] == 0 and not board[0][0].castled:
                        moves.append((2, 0))
                        moves.append((3, 0))
            else:
                if board[7][7] != 0:
                    if board[5][7] == 0 and board[6][7] == 0 and not board[7][7].castled:
                        moves.append((5, 7))
                        moves.append((6, 7))
                if board[0][7] != 0:
                    if board[1][7] == 0 and board[2][7] == 0 and board[3][7] == 0 and not board[0][7].castled:
                        moves.append((2, 7))
                        moves.append((3, 7))



        return moves

class Bishop(Piece):
    def get_danger_moves(self, board):
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

    def get_danger_moves(self, board):
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

    def get_danger_moves(self, board):
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

    def promote(self):
        self.promoted = True
        self.sign = 'Q'
        if self.color == BLACK:
            self.img = BLACK_QUEEN
        else:
            self.img = WHITE_QUEEN
        self.img = pygame.image.load(self.img)
        self.img = pygame.transform.scale(self.img, (W, W))
    
    def get_danger_moves(self, board):
        moves = []
        i, j = self.col, self.row
        if self.color == BLACK:
            if i + 1 < 8:
                if board[i + 1][j + 1] != 0:
                    moves.append((i + 1, j + 1))

            if i - 1 > -1:
                if board[i - 1][j + 1] != 0:
                    moves.append((i - 1, j + 1))

        else:
            if i + 1 < 8:
                if board[i + 1][j - 1] != 0:
                    moves.append((i + 1, j - 1))
            if i - 1 > -1:
                if board[i - 1][j - 1] != 0:
                    moves.append((i - 1, j - 1))
        return moves


    def get_valid_moves(self, board):
        moves = []
        i, j = self.col, self.row
        if self.color == BLACK:
            if i + 1 <= 7:
                if board[i + 1][j + 1] != 0:
                    if board[i + 1][j + 1].color != self.color:
                        moves.append((i + 1, j + 1))
            if i - 1 >= 0:
                if board[i - 1][j + 1] != 0:
                    if board[i - 1][j + 1].color != self.color:
                        moves.append((i - 1, j + 1))
            if self.first:
                if board[i][j + 1] == 0:
                    moves.append((i, j + 1))
                    if board[i][j + 2] == 0:
                        moves.append((i, j + 2))
            else:
                if board[i][j + 1] == 0:
                    moves.append((i, j + 1))
        
        else:
            if i + 1 <= 7:
                if board[i + 1][j - 1] != 0:
                    if board[i + 1][j - 1].color != self.color:
                        moves.append((i + 1, j - 1))
            if i - 1 >= 0:
                if board[i - 1][j - 1] != 0:
                    if board[i - 1][j - 1].color != self.color:
                        moves.append((i - 1, j - 1))
            if self.first:
                if board[i][j - 1] == 0:
                    moves.append((i, j - 1))
                    if board[i][j - 2] == 0:
                        moves.append((i, j - 2))
            else:
                if board[i][j - 1] == 0:
                    moves.append((i, j - 1))
                    

        return moves
                

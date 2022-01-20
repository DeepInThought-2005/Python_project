import pygame
from constants import *
from pieces import *

class Board:
    def __init__(self) -> None:
        self.moves_50 = 0
        self.repetition = 0
        self.board = [[0] * 8 for _ in range(8)]
        self.boardstyle = BOARDSTYLE
        self.board_img = pygame.transform.scale(pygame.image.load(
            os.path.join("Image/Boards", BOARDSTYLE+FILETYPE)), (DEF_WIDTH, DEF_HEIGHT))
        self.generate_initial()

    def resize(self, w, h):
        self.board_img = self.board_img = pygame.transform.scale(pygame.image.load(
            os.path.join("Image/Boards", BOARDSTYLE+FILETYPE)), (w, h))

    def resize_pieces(self, w, h):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.board[i][j].resize(w, h)

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

    def change_turn(self, turn):
        if turn == BLACK:
            turn = WHITE
        else:
            turn = BLACK
        return turn

    def get_valid_moves(self, turn):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == turn:
                        for move in self.board[i][j].get_valid_moves(self):
                            moves.append([(i, j), move])
        return moves

    def get_danger_moves(self, turn, for_checkmate=False):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == turn:
                        if for_checkmate:
                            if isinstance(self.board[i][j], Pawn):
                                for move in self.board[i][j].get_valid_moves(self):
                                    moves.append([(i, j), move])
                            else:
                                if not isinstance(self.board[i][j], King):
                                    for move in self.board[i][j].get_danger_moves(self):
                                        moves.append([(i, j), move])

                        if not for_checkmate:
                            for move in self.board[i][j].get_danger_moves(self):
                                moves.append(move)


        return moves

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
            return chr(ord('a') + pos1[0]) + str(8 - pos1[1]) + '-' + chr(ord('a') + pos2[0]) + str(8 - pos2[1])

    def is_legal_move(self, turn, start, end, for_checkmate=False):
        tboard = Board()
        tboard.board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                tboard.board[i][j] = self.board[i][j]

        if not for_checkmate:
            if not isinstance(tboard.board[end[0]][end[1]], King):
                tboard.move(start, end)
                turn = self.change_turn(turn)
                if tboard.check(turn):
                    tboard.move(end, start)
                    return False
                tboard.move(end, start)
                return True
        else:
            if not isinstance(tboard.board[end[0]][end[1]], King):
                tboard.move(start, end)
                turn = self.change_turn(turn)
                if tboard.check(turn):
                    tboard.move(end, start)
                    return False
                tboard.move(end, start)
                return True

    def draw_valid_moves(self, win, moves, turn, w, h):
        if moves:
            for move in moves:
                if self.board[move[0]][move[1]] == 0:
                    pygame.draw.circle(win, valid_move_color, (move[0] * w + w // 2, move[1] * h + h // 2), w // 5)
                else:
                    if turn != self.board[move[0]][move[1]].color:
                        pygame.draw.rect(win, valid_move_color, (move[0] * w, move[1] * h, w, h), 4)


    def generate_initial(self):
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

    def draw_pieces(self, win):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)

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
        print()


    def checkdraw(self):
        # check 50 moves rule
        if self.moves_50 == 50:
            return True

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

    def stalemate(self, turn):
        if not self.check(turn):
            valid_king_moves = []
            danger_moves = self.get_danger_moves(turn)
            for i in range(8):
                for j in range(8):
                    if isinstance(self.board[i][j], King):
                        if turn != self.board[i][j].color:
                            for move in self.board[i][j].get_valid_moves(self):
                                valid_king_moves.append(move)
            valid_moves = self.get_valid_moves(self.change_turn(turn))

            # if king can move
            if len(valid_moves) - len(valid_king_moves) == 0:
                for move in valid_king_moves:
                    if move not in danger_moves:
                        return False
                return True



    def checkmate(self, turn):
        king_pos = self.get_king_pos(turn)
        danger_moves = self.get_danger_moves(turn)
        checkers = self.get_checkers(turn)
        defend_moves = self.get_danger_moves(self.change_turn(turn), for_checkmate=True)
        valid_king_moves = []
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], King):
                    if turn != self.board[i][j].color:
                        for move in self.board[i][j].get_valid_moves(self):
                            valid_king_moves.append(move)

        if self.check(turn):
            # if checker can be captured
            if len(checkers) != 2:
                for checker in checkers:
                    for d_m in defend_moves:
                        if checker == d_m[1]:
                            print("Checker can be captured")
                            return False

            # if king can move
            for move in valid_king_moves:
                if move not in danger_moves:
                    if self.is_legal_move(self.change_turn(turn), king_pos, move):
                        print("King has safe square")
                        return False

            # if something can block
            if len(checkers) != 2:
                checker_danger_moves = self.board[checkers[0][0]][checkers[0][1]].get_danger_moves(self)
                for move in defend_moves:
                    if move[1] in checker_danger_moves:
                        if self.is_legal_move(self.change_turn(turn), move[0], move[1], for_checkmate=True):
                            print("The check can be blocked")
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
        win.blit(self.board_img, (0, 0))

    def draw_pieces(self, win):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)

    def get_king_pos(self, turn):
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], King):
                    if turn != self.board[i][j].color:
                        king_pos = (i, j)
                        return king_pos
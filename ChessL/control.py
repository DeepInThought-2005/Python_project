from tkinter.constants import MOVETO
from pieces import *
import random
from board import *
pygame.font.init()


class Control:
    def __init__(self, board) -> None:
        self.board = board
        self.turn = WHITE
        board.print_board()
        self.marked_pos = [[0] * 8 for _ in range(8)]
        self.selected_pos = ()
        self.valid_moves = []
        self.gameoverd = False
        self.en_passant_pos = ()
        self.move_text = ""
        self.repeated = 0

    def switch_turn(self, turn):
        if turn == WHITE:
            turn = BLACK
        else:
            turn = WHITE

        return turn
        
    def AI_move(self, depth=2):
        def evaluate():
            score = self.bard.get_score()
        moves = self.board.get_valid_moves(self.turn)
        best_move = []
        # valid moves
        vm = []
        tboard = self.create_tboard(self.board.board)
        for move in moves:
            captured = tboard.board[move[1][0]][move[1][1]]
            tboard.move(move[0], move[1])
            if not tboard.check(self.switch_turn(self.turn)):
                vm.append(move)
            tboard.move(move[1], move[0], captured)


        if not self.check_gameover(self.turn) and vm:
            for m in vm:
                score1 = tboard.get_score()
                captured = tboard.board[m[1][0]][m[1][1]]
                tboard.move(m[0], m[1])
                score2 = tboard.get_score()
                if score2 == score1:
                    best_move = m

                if score2 < score1:
                    best_move = m
                    return best_move

                tboard.move(m[1], m[0], captured)
            
            best_move = random.choice(vm)

        return best_move

    def make_move(self, start, end):
        '''
        returns tuple including start position and end position
        '''
        s_x, s_y = start
        e_x, e_y = end
        bo = self.board.board
        pro_square = bo[e_x][e_y]
        self.board.board[e_x][e_y] = self.board.board[s_x][s_y]
        self.board.board[e_x][e_y].col = e_x
        self.board.board[e_x][e_y].row = e_y
        self.board.board[s_x][s_y] = 0

        if isinstance(bo[end[0]][end[1]], Rook):
            self.board.board[end[0]][end[1]].castled = True

        if isinstance(bo[end[0]][end[1]], King):
            if not bo[end[0]][end[1]].castled:
                self.move_text = self.maybe_castles(start, end)
            self.board.board[e_x][e_y].castled = True

        if isinstance(bo[end[0]][end[1]], Pawn):
            if self.board.board[end[0]][end[1]] != 0:
                self.board.board[end[0]][end[1]].first = False
                self.maybe_enpassant(start, end)
                self.moves_50 = 0


            if end[1] == 7 or end[1] == 0:
                if not self.board.board[end[0]][end[1]].promoted:
                    self.board.board[end[0]][end[1]].promote(start[0], start[1])
                    if not self.board.board[end[0]][end[1]].promoted:
                        self.board.board[s_x][s_y] = self.board.board[e_x][e_y]
                        self.board.board[e_x][e_y] = pro_square
                    else:
                        self.moves_50 = 0
                        

        
        # set en_passant_pos
        if abs(end[1] - start[1]) == 2:
            self.en_passant_pos = (end[0], end[1])
        else:
            self.en_passant_pos = ()
        self.board.set_every_pos()

        self.board.print_board()

    def game_over(self, win, w, h, tie=False, stalemate=False):
        #START_END.play()
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
        win.blit(text, (w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2))
        win.blit(hint, (w // 2 - hint.get_width() // 2, h // 4 * 3 - text.get_height() // 2))
        pygame.display.update()
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True
    
    def print_board(self, board):
        for i in range(8):
            for j in range(8):
                if board[j][i] != 0:
                    font_color = ''
                    if board[j][i].color == WHITE:
                        font_color = '37m'
                    else:
                        font_color = '31m'
                    print("\033[1;" + font_color + board[j][i].sign + "\033[0m", end=' ')
                else:
                    print('.', end=' ')
            print()
        print()

    def create_tboard(self, bo):
        tboard = Board()
        tboard.board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                tboard.board[i][j] = bo[i][j]
        return tboard

    
    def maybe_enpassant(self, selected_pos, moved_pos):
        x, y = moved_pos
        if self.board.board[x][y].is_move_en_passant(selected_pos, self.en_passant_pos):
            if moved_pos[0] == self.en_passant_pos[0]:
                if self.turn == BLACK:
                    self.board.board[x][y - 1] = 0
                else:
                    self.board.board[x][y + 1] = 0
                #CAPTURE.play()


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
        return moves
    
    def check_gameover(self, color):
        if self.board.checkmate(color):
            return CHECKMATE
        if self.board.stalemate(color):
            return STALEMATE
        if self.board.checkdraw():
            return DRAW
        return None

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_color(self, win, hell_color, dark_color, pos, w, h):
        x, y = pos
        if x % 2 == 0:
            if y % 2 != 0:
                pygame.draw.rect(win, dark_color, (x * w, y * h, w, h))
            if y % 2 == 0:
                pygame.draw.rect(win, hell_color, (x * w, y * h, w, h))
        else:
            if y % 2 == 0:
                pygame.draw.rect(win, dark_color, (x * w, y * h, w, h))
            if y % 2 != 0:
                pygame.draw.rect(win, hell_color, (x * w, y * h, w, h))


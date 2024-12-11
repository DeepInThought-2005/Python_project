from copy import deepcopy
import tkinter as tk
from random import *
from tkinter import messagebox

from Constants import *

class BoardCanvas(tk.Canvas):
    def __init__(self, root:App):
        super().__init__(root)
        self.r = root
        self._padx = 10 # distance from screen
        self.configure(highlightthickness=1, highlightbackground="black",  
                       width=WIN_WIDTH-self._padx*2, height=WIN_WIDTH-self._padx*2)   
        self.turn = B
        self.col = 8
        self.row = 8
        self.weight_table = generate_weight_board(self.col, self.row)
        self.mode = HUMAN_HUMAN
        self.play_as = B
        self.depth = 3
        self.calculating = False # solves undo redo problem
        self.game_state = "" # win or lose or draw or Zugzwang

        self.show_vm_as = EVAL
        self.is_draw_valid_moves = True
        self.is_animating_flip = True

        self.init_board(self.col, self.row)

        # self.bind("<Button-1>", self.clicked)
        self.bind("<Motion>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
    
    def init_board(self, col, row):
        self.turn = B
        self.array = [[EMPTY for i in range(self.row)] for j in range(self.col)]
        tc = col // 2
        tr = row // 2
        self.array[tc-1][tr-1] = W
        self.array[tc][tr-1] = B
        self.array[tc-1][tr] = B
        self.array[tc][tr] = W
        self.pieces_left = {W:self.col*self.row//2 - 2, B:self.col*self.row//2 - 2}
        self.black_left = self.col*self.row//2 - 2
        self.white_left = self.col*self.row//2 - 2
        self.undo_array = [deepcopy(self.array)]
        self.redo_array = []
        self.valid_moves = self.get_valid_moves(self.array, self.turn)
        self.hover_pos = (0, 0)
        self.capturable_list = self.get_capturable(self.array, self.turn, self.valid_moves) # amount of capturable pieces in every valid moves
        self.reset_eval_list()
        self.animating = False # for on_hover purpose
        self.redraw()

    def on_hover(self, event):
        x = int(event.x // (self.winfo_width() / self.col))
        y = int(event.y // (self.winfo_height() / self.row))
        if (x, y) in self.valid_moves and not self.animating:
            self.configure(cursor="hand2")
            if self.is_draw_valid_moves:
                size = min(self.r.winfo_height(), self.r.winfo_width()) // 30
                if self.show_vm_as == DOT:
                    self.delete("hover")
                    mulp = 0.1
                    self.draw_circle(x, y, self.turn, self.turn, mulp, "hover")
                    self.hover_pos = (x, y)
                elif self.show_vm_as == CAPTURABLE:
                    self.delete("hover")
                    self.place_text(x, y, self.capturable_list[(x, y)], size, "#FFA500", "hover")
                elif self.show_vm_as == EVAL:
                    self.delete("hover")
                    self.place_text(x, y, self.eval_list[(x, y)], size, "#FFA500", "hover")    

        else:
            self.configure(cursor="arrow")
            self.delete("hover")
    
    def clicked(self, event):
        x = int(event.x // (self.winfo_width() / self.col))
        y = int(event.y // (self.winfo_height() / self.row))
        if x < self.col and y < self.row:
            to_flip = self.is_valid_move(self.array, self.turn, x, y)
            if to_flip:
                if self.is_animating_flip:
                    self.animate_move(self.array, x, y, self.turn)
                else:
                    self.apply_move(self.array, x, y, self.turn)
                    
                self.switch_turn()
                # self.redraw()
                self.update()
                self.valid_moves = self.get_valid_moves(self.array, self.turn)
                if self.valid_moves:
                    pass
                else:
                    self.update_game_state()
                        
                self.capturable_list = self.get_capturable(self.array, self.turn, self.valid_moves)
                self.reset_eval_list()
                self.print_board(self.array)

                if self.mode == HUMAN_AI:
                    self.AI_move()
                    self.redraw()
                    self.update()
                    self.print_board(self.array)

    def update_game_state(self):
        self.switch_turn()
        self.valid_moves = self.get_valid_moves(self.array, self.turn)
        if not self.valid_moves:
            wl = self.get_pieces_left(W)
            bl = self.get_pieces_left(B)
            if wl > bl:
                self.game_state = WHITE_WINS
            elif wl < bl:
                self.game_state = BLACK_WINS
            else:
                self.game_state = DRAW
        else:
            if self.turn == W:
                self.game_state = ZUGZWANG_WHITE
            else:
                self.game_state = ZUGZWANG_BLACK
    
    def reset_eval_list(self):
        self.calculating = True
        self.update()
        self.eval_list = self.minimax(self.array, self.depth, True, self.turn, -INF, INF, self.determine_stage(self.array))[1]
        # self.update()
        self.calculating = False
                    
    def apply_move(self, board, col, row, turn):
        # apply move without animation
        to_flip = self.is_valid_move(board, turn, col, row)
        if not self.calculating:
            self.undo_array.append(deepcopy(board))
            self.redo_array = [] # reset redo array
        board[col][row] = turn
        for move in to_flip:
            board[move[0]][move[1]] = turn
        return board

    def animate_move(self, board, x, y, turn):
        # apply move with animation
        to_flip = self.is_valid_move(board, turn, x, y)
        if not self.calculating:
            self.undo_array.append(deepcopy(board))
            self.redo_array = [] # reset redo array
        board[x][y] = self.turn
        self.is_draw_valid_moves = False
        self.redraw()
        for move in to_flip:
            self.flip_piece(board, move[0], move[1])
        self.pieces_left[self.turn] -= 1
        self.is_draw_valid_moves = True
        return board


    def on_leave(self, event):
        self.delete("hover")


    def get_capturable(self, arr, turn, valid_mv):
        to_return = {}
        for move in valid_mv:
            to_return[move] = len(self.is_valid_move(arr, turn, move[0], move[1]))   
        return to_return
            

    def pack_self(self):
        self.pack(expand=True)

    def switch_turn(self):
        if self.turn == W:
            self.turn = B
        else:
            self.turn = W

    def redraw(self):
        self.delete(tk.ALL)
        self.draw_board()
        self.draw_pieces()
        self.draw_valid_moves(self.valid_moves)

    def get_pieces_left(self, color=None):
        result = 0
        if color == B:
            result = len(self.get_all_pos(B))
        elif color == W:
            result = len(self.get_all_pos(W))
        else:
            result = len(self.get_all_pos(W))+len(self.get_all_pos(B))
        
        return result


    def undo(self):
        if len(self.undo_array) > 1:
            self.redo_array.append(deepcopy(self.array))
            self.array = deepcopy(self.undo_array.pop())
            self.switch_turn()
            self.valid_moves = self.get_valid_moves(self.array, self.turn)
            self.capturable_list = self.get_capturable(self.array, self.turn, self.valid_moves)
            self.reset_eval_list()
            self.redraw()

    def redo(self):
        if len(self.redo_array) > 0:
            self.undo_array.append(deepcopy(self.array))
            self.array = deepcopy(self.redo_array.pop())
            self.switch_turn()
            self.valid_moves = self.get_valid_moves(self.array, self.turn)
            self.capturable_list = self.get_capturable(self.array, self.turn, self.valid_moves)
            self.reset_eval_list()
            self.redraw()
    
    def flip_piece(self, arr, col, row):
        if arr[col][row] == W:
            self.animate_flip(col, row, self.turn)
            arr[col][row] = B
        else:
            self.animate_flip(col, row, self.turn)
            arr[col][row] = W

    def animate_flip(self, col, row, turn):       
        mulp = 0.08
        if turn == W:
            t = B
        else:
            t = W

        r = 24 # i in range(r)
        self.animating = True

        self.delete("{0}-{1}".format(col, row))
        #shrinking
        for i in range(r):
            self.create_oval(col * self.get_cell_width()+i*self.get_cell_width()//2//r,
                            row * self.get_cell_height()+i*self.get_cell_height()//2//r,
                            (col+1) * self.get_cell_width()-i*self.get_cell_width()//2//r,
                            (row+1) * self.get_cell_height()-i*self.get_cell_height()//2//r,
                            fill=t, tags="animated")
            if i % 2 == 0:
                self.after(2)
            self.update()
            self.delete('animated')

        #expanding
        for i in range(r):
            self.create_oval(col * self.get_cell_width()+self.get_cell_width()//2-i*self.get_cell_width()//2//r,
                            row * self.get_cell_height()+self.get_cell_height()//2-i*self.get_cell_height()//2//r,
                            (col+1) * self.get_cell_width()-self.get_cell_width()//2+i*self.get_cell_width()//2//r,
                            (row+1) * self.get_cell_height()-self.get_cell_height()//2+i*self.get_cell_height()//2//r,
                            fill=turn, tags="animated")
            if i % 2 == 0:
                self.after(2)
            self.update()
            self.delete('animated')
        
        self.draw_piece(col, row, turn)

        self.animating = False

    def get_all_pos(self, color):
        #returns all (color) pieces positions
        pos = []
        for i in range(self.row):
            for j in range(self.col):
                if self.array[j][i] == color:
                    pos.append((j, i))
        return pos
    
    def is_on_board(self, col, row):
        if col < self.col and col >= 0 and row < self.row and row >= 0:
            return True
        else:
            return False

    def is_valid_move(self, array, turn, xstart, ystart):
        if array[xstart][ystart] != -1:
            return False
        
        if turn == W:
            otherTurn = B
        else:
            otherTurn = W
        
        array[xstart][ystart] = turn
        tilesToFlip = []

        for xdir, ydir in [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]:
            x=xstart
            y=ystart
            x += xdir
            y += ydir
            if self.is_on_board(x, y) and array[x][y] == otherTurn:
                x += xdir
                y += ydir
                if not self.is_on_board(x, y):
                    continue
                while array[x][y] == otherTurn:
                    x += xdir
                    y += ydir
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
                    continue
                if array[x][y] == turn:
                    while True:
                        x -= xdir
                        y -= ydir
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append((x, y))
        array[xstart][ystart] = -1 # restore the empty space
        if len(tilesToFlip) == 0:
            return False
        return tilesToFlip   
                   
    def get_valid_moves(self, array, turn):
        moves = []
        for i in range(self.row):
            for j in range(self.col):
                if self.is_valid_move(array, turn, j, i):
                    moves.append((j, i))
        return moves

    def draw_valid_moves(self, moves):
        if self.is_draw_valid_moves and not self.calculating:
            for move in moves:
                self.draw_valid_move(move[0], move[1])

    def draw_valid_move(self, col, row):
        c = '#98FF98'
        size = min(self.r.winfo_height(), self.r.winfo_width()) // 30

        if self.show_vm_as == EVAL:
            self.place_text(col, row, self.eval_list[(col, row)], size)
        elif self.show_vm_as == CAPTURABLE:
            self.place_text(col, row, self.capturable_list[(col, row)], size)
        elif self.show_vm_as == DOT:
            mulp = 0.15
            self.draw_circle(col, row, c, c, mulp)
    
    def place_text(self, col, row, txt, size, _color="black",  _tag=None):
        mulp = 0.1
        self.create_text(col * self.get_cell_width()+self.get_cell_width() / 2,
                         row * self.get_cell_height()+self.get_cell_height() / 2,
                        text=txt, font=("Helvetica", size), tag=_tag, fill=_color)
        
    def draw_circle(self, col, row, _fill, _outline, mulp, _tag=None):
        self.create_oval(col * self.get_cell_width()+self.get_cell_width()*mulp,
                         row * self.get_cell_height()+self.get_cell_height()*mulp,
                         (col+1) * self.get_cell_width()-self.get_cell_width()*mulp,
                         (row+1) * self.get_cell_height()-self.get_cell_height()*mulp,
                         fill=_fill, outline=_outline, tag=_tag)
    
    def draw_board(self):
        # height_multiplier = float(self.winfo_height() / self.row)
        # width_multiplier = float(self.winfo_width() / self.col)
        # for row in range(self.row):
        #     self.create_line(0, row*height_multiplier, self.winfo_width(), row*height_multiplier)
        # for col in range(self.col):
        #     self.create_line(col*width_multiplier, 0, col*width_multiplier, self.winfo_height())


        cell_width = self.winfo_width() / self.col
        cell_height = self.winfo_height() / self.row


        # '#006400', '#8FBC8F'
        dark_color='#006400'
        light_color='#8FBC8F'

        # Create the grid
        for row in range(self.row):
            for col in range(self.col):
                x1 = col * cell_width
                y1 = row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                color = dark_color if (row + col) % 2 == 0 else light_color
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
    
    def draw_pieces(self):
        for i in range(self.row):
            for j in range(self.col):
                    if self.array[j][i] != -1:
                        self.draw_piece(j, i, self.array[j][i])
    
    def draw_piece(self, col, row, color):
        mulp = 0.08
        self.create_oval(col * self.get_cell_width()+self.get_cell_width()*mulp,
                         row * self.get_cell_height()+self.get_cell_height()*mulp,
                         (col+1) * self.get_cell_width()-self.get_cell_width()*mulp,
                         (row+1) * self.get_cell_height()-self.get_cell_height()*mulp,
                         fill=color, tags="tile {0}-{1}".format(col,row), outline=color)

    def get_cell_width(self):
        return self.winfo_width() / self.col
    
    def get_cell_height(self):
        return self.winfo_height() / self.row
    
    def print_board(self, arr):
        for i in range(2*self.col):
            print('-', end="")
        print()
        for i in range(self.row):
            for j in range(self.col):
                if arr[j][i] == EMPTY:
                    print('o ', end="")
                elif arr[j][i] == W:
                    print('W ', end="")
                else:
                    print('B ', end="")
            print()
        for i in range(2*self.col):
            print('-', end="")
        print()

    def determine_stage(self, board):
        total_discs = sum(cell != EMPTY for row in board for cell in row)
        if total_discs <= self.row*self.col // 3:
            return "opening"
        elif total_discs <= self.row*self.col // 5 * 4:
            return "midgame"
        else:
            return "endgame"

    def evaluate(self, board, turn, stage):
        opponent = B if turn == W else W
        player_score = 0
        opponent_score = 0

        for row in range(self.row):
            for col in range(self.col):
                if board[col][row] == turn:
                    if stage == "opening":
                        player_score += self.weight_table[col][row]
                    elif stage == "midgame":
                        player_score += self.weight_table[col][row] // 2
                    else:  # endgame
                        player_score += 1
                elif board[col][row] == opponent:
                    if stage == "opening":
                        opponent_score += self.weight_table[col][row]
                    elif stage == "midgame":
                        opponent_score += self.weight_table[col][row] // 2
                    else:  # endgame
                        opponent_score += 1

        return player_score - opponent_score
        
    def minimax(self, board, depth, maximizing_player, turn, alpha, beta, stage):
        opponent = B if turn == W else B
        if maximizing_player:
            valid_moves = self.get_valid_moves(board, turn)
        else:
            valid_moves = self.get_valid_moves(board, opponent)
        
        if depth == 0 or not valid_moves:
            return self.evaluate(board, turn, stage), []
        
        move_evaluations = {}
        
        if maximizing_player:
            max_eval = -INF
            for move in valid_moves:
                new_board = self.apply_move([row[:] for row in board], move[0], move[1], turn)
                eval, _ = self.minimax(new_board, depth - 1, False, turn, alpha, beta, self.determine_stage(new_board))
                move_evaluations[move] = eval
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, move_evaluations
        else:
            min_eval = INF
            for move in valid_moves:
                new_board = self.apply_move([row[:] for row in board], move[0], move[1], opponent)
                eval, _ = self.minimax(new_board, depth - 1, True, turn, alpha, beta, self.determine_stage(new_board))
                move_evaluations[move] = eval
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, move_evaluations
    
    def AI_move(self):
        if not self.animating:
            # make a move with AI
            max_value = -INF
            max_key = ()
            for key, value in self.eval_list.items():
                if value > max_value:
                    max_value = value
                    max_key = key

            to_flip = self.is_valid_move(self.array, self.turn, max_key[0], max_key[1])
            if to_flip:
                if self.is_animating_flip:
                    self.animate_move(self.array, max_key[0], max_key[1], self.turn)
                else:
                    self.apply_move(self.array, max_key[0], max_key[1], self.turn)

            self.switch_turn()

            self.valid_moves = self.get_valid_moves(self.array, self.turn)
            if self.valid_moves:
                pass
            else:
                self.update_game_state()

            self.valid_moves = self.get_valid_moves(self.array, self.turn)
            self.capturable_list = self.get_capturable(self.array, self.turn, self.valid_moves)
            self.reset_eval_list()
            self.redraw()

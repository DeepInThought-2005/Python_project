import tkinter as tk
import os
from PIL import ImageTk, Image

'''
i is row
j is col
'''

# Constant
IMG_SIZE = 100

class Othello:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.setup()
        self.packall()
        self.root.mainloop()

    def setup(self):
        self.turn = 0
        self.valid_moves = []
        self.restart = tk.Button(self.root, text="restart", font=("Arial", 16),
                                 bd=4, command=self.reset)
        self.black = 2
        self.white = 2
        self.black_label = tk.Label(self.root, text=self.black, font=("Arial", 14))
        self.white_label = tk.Label(self.root, text=self.white, font=("Arial", 14))
        self.turn_label = tk.Label(self.root, text="Black to move...", font=("Arial", 14))
        # imgs
        self.b = Image.open('img\\black_circle.png')
        self.b = self.b.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
        self.b = ImageTk.PhotoImage(self.b)
        self.w = Image.open('img\\white_circle.png')
        self.w = self.w.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
        self.w = ImageTk.PhotoImage(self.w)
        self.blank = Image.open('img\\blank.png')
        self.blank = self.blank.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
        self.blank = ImageTk.PhotoImage(self.blank)
        self.valid_sign = Image.open('img\\valid_move.png')
        self.valid_sign = self.valid_sign.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
        self.valid_sign = ImageTk.PhotoImage(self.valid_sign)

        self.board = [[-1 for i in range(8)] for j in range(8)]
        self.set_origi_pos()

        self.buttons = [[tk.Button(self.root, width=100, height=100, bd=4,
                            image=self.blank, relief=tk.RIDGE, activebackground="red")
                            for i in range(8)]
                            for j in range(8)]
        for i in range(8):
            for j in range(8):
                self.buttons[i][j]['command'] = lambda id=i*8+j: self.button_onclick(id)

        self.upgrade()

    def packall(self):
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].grid(column=j, row=i)

        self.restart.grid(column=8, row=0, padx=10)
        self.black_label.grid(column=8, row=6, padx=10)
        self.white_label.grid(column=8, row=7, padx=10)
        self.turn_label.grid(column=8, row=1, padx=10)


    def set_origi_pos(self):
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[3][4] = 0
        self.board[4][3] = 0

    def reset(self):
        for i in range(8):
            for j in range(8):
                self.board[i][j] = -1
        self.black = 2
        self.white = 2
        self.set_origi_pos()
        self.upgrade()

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.buttons[i][j]['image'] = self.blank
                self.buttons[i][j]['activebackground'] = 'red'

    def count(self):
        self.black = 0
        self.white = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    self.black += 1
                elif self.board[i][j] == 1:
                    self.white += 1


    def upgrade(self):
        self.clear_board()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    self.buttons[i][j]['image'] = self.b
                elif self.board[i][j] == 1:
                    self.buttons[i][j]['image'] = self.w
                else:
                    self.buttons[i][j]['image'] = None

        self.valid_moves = self.get_valid_moves()
        for move in self.valid_moves:
            if move:
                self.buttons[move[0]][move[1]]['image'] = self.valid_sign
                self.buttons[move[0]][move[1]]['activebackground'] = "green"

        self.count()
        self.black_label['text'] = "black: " + str(self.black)
        self.white_label['text'] = "white: " + str(self.white)


    def button_onclick(self, id, event=None):
        i = id // 8
        j = id %  8
        if (i, j) in self.valid_moves:
            self.board[i][j] = self.turn
            moves = self.get_capture(i, j)
            print(moves)
            for move in moves:
                self.board[move[0]][move[1]] = \
                self.turn_changer(self.board[move[0]][move[1]])
            self.change_turn()
            self.upgrade()
            self.count()

    def turn_changer(self, t):
        if t == 0:
            t = 1
        else:
            t = 0
        return t

    def change_turn(self):
        if self.turn == 0:
            self.turn = 1
            self.turn_label['text'] = "White to move..."
        else:
            self.turn = 0
            self.turn_label['text'] = "Black to move..."

    def get_valid_moves(self):
        def down(i, j):
            move = ()
            x = i
            while x < 6 and self.board[x + 1][j] != self.turn and self.board[x + 1][j] != -1:
                x += 1
            if x < 7 and self.board[x + 1][j] == -1 and x != i:
                move = (x + 1, j)

            return move

        def up(i, j):
            move = ()
            x = i
            while x > 1 and self.board[x - 1][j] != self.turn and self.board[x - 1][j] != -1:
                x -= 1
            if x > 0 and self.board[x - 1][j] == -1 and x != i:
                move = (x - 1, j)

            return move

        def left(i, j):
            move = ()
            x = j
            while x > 1 and self.board[i][x - 1] != self.turn and self.board[i][x - 1] != -1:
                x -= 1
            if x > 0 and self.board[i][x - 1] == -1 and x != j:
                move = (i, x - 1)

            return move

        def right(i, j):
            move = ()
            x = j
            while x < 6 and self.board[i][x + 1] != self.turn and self.board[i][x + 1] != -1:
                x += 1
            if x < 7 and self.board[i][x + 1] == -1 and x != j:
                move = (i, x + 1)

            return move

        def left_up(i, j):
            move = ()
            x = j
            y = i
            while x > 1 and y > 1 and self.board[y - 1][x - 1] != self.turn and self.board[y - 1][x - 1] != -1:
                x -= 1
                y -= 1
            if y > 0 and x > 0 and self.board[y - 1][x - 1] == -1 and x != j and y != i:
                move = (y - 1, x - 1)

            return move

        def left_down(i, j):
            move = ()
            x = j
            y = i
            while x > 1 and y < 6 and self.board[y + 1][x - 1] != self.turn and self.board[y + 1][x - 1] != -1:
                x -= 1
                y += 1
            if x > 0 and y < 7 and self.board[y + 1][x - 1] == -1 and x != j and y != i:
                move = (y + 1, x - 1)

            return move

        def right_up(i, j):
            move = ()
            x = j
            y = i
            while x < 6 and y > 1 and self.board[y - 1][x + 1] != self.turn and self.board[y - 1][x + 1] != -1:
                x += 1
                y -= 1
            if x < 7 and y > 0 and self.board[y - 1][x + 1] == -1 and x != j and y != i:
                move = (y - 1, x + 1)

            return move

        def right_down(i, j):
            move = ()
            x = j
            y = i
            while x < 6 and y < 6 and self.board[y + 1][x + 1] != self.turn and self.board[y + 1][x + 1] != -1:
                x += 1
                y += 1
            if x < 7 and y < 7 and self.board[y + 1][x + 1] == -1 and x != j and y != i:
                move = (y + 1, x + 1)

            return move

        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.turn:
                    moves.append(down(i, j))
                    moves.append(up(i, j))
                    moves.append(left(i, j))
                    moves.append(right(i, j))
                    moves.append(left_up(i, j))
                    moves.append(left_down(i, j))
                    moves.append(right_up(i, j))
                    moves.append(right_down(i, j))
        return moves

    def get_capture(self, i, j):
        '''
        everything should be fliped!
        '''
        moves = []
        def down():
            x = i
            while x > 1 and self.board[x - 1][j] not in (self.turn, -1):
                x -= 1
            if i - x > 0 and self.board[x - 1][j] != -1:
                return True

        def up():
            x = i
            while x < 6 and self.board[x + 1][j] not in (self.turn, -1):
                x += 1
            if x - i > 0 and self.board[x + 1][j] != -1:
                return True

        def left():
            x = j
            while x < 6 and self.board[i][x + 1] not in (self.turn, -1):
                x += 1
            if x - j > 0 and self.board[i][x + 1] != -1:
                return True

        def right():
            x = j
            while x > 1 and self.board[i][x - 1] not in (self.turn, -1):
                x -= 1
            if j - x > 0 and self.board[i][x - 1] != -1:
                return True

        def left_up():
            x = j
            y = i
            while x < 6 and y < 6 and self.board[y + 1][x + 1] not in (self.turn, -1):
                x += 1
                y += 1
            if x - j > 0 and y - i > 0 and self.board[y + 1][x + 1] != -1:
                return True

        def left_down():
            x = j
            y = i
            while x < 6 and y > 1 and self.board[y - 1][x + 1] not in (self.turn, -1):
                x += 1
                y -= 1
            if x - j > 0 and i - y > 0 and self.board[y - 1][x + 1] != -1:
                return True

        def right_up():
            x = j
            y = i
            while x > 1 and y < 6 and self.board[y + 1][x - 1] not in (self.turn, -1):
                x -= 1
                y += 1
            if j - x > 0 and y - i > 0 and self.board[y + 1][x - 1] != -1:
                return True

        def right_down():
            x = j
            y = i
            while x > 1 and y > 1 and self.board[y - 1][x - 1] not in (self.turn, -1):
                x -= 1
                y -= 1
            if j - x > 0 and i - y > 0 and self.board[y - 1][x - 1] != -1:
                return True

        #################################################################################

        if up():
            print("up")
            x = i
            while self.board[x + 1][j] != self.turn:
                x += 1
                moves.append((x, j))

        if down():
            print("down")
            x = i
            while self.board[x - 1][j] != self.turn:
                x -= 1
                moves.append((x, j))

        if left():
            print("left")
            x = j
            while x < 6 and self.board[i][x + 1] not in (self.turn, -1):
                x += 1
                moves.append((i, x))

        if right():
            print("right")
            x = j
            while x > 1 and self.board[i][x - 1] not in (self.turn, -1):
                x -= 1
                moves.append((i, x))

        if left_up():
            print("left_up")
            x = j
            y = i
            while x < 6 and y < 6 and self.board[y + 1][x + 1] not in (self.turn, -1):
                x += 1
                y += 1
                moves.append((y, x))

        if left_down():
            print('left_down')
            x = j
            y = i
            while x < 6 and y > 1 and self.board[y - 1][x + 1] not in (self.turn, -1):
                x += 1
                y -= 1
                moves.append((y, x))

        if right_up():
            print('right_up')
            x = j
            y = i
            while x > 1 and y < 6 and self.board[y + 1][x - 1] not in (self.turn, -1):
                x -= 1
                y += 1
                moves.append((y, x))

        if right_down():
            print('right_down')
            x = j
            y = i
            while x > 1 and y > 1 and self.board[y - 1][x - 1] not in (self.turn, -1):
                x -= 1
                y -= 1
                moves.append((y, x))


        return moves


if __name__ == "__main__":
    othello = Othello()

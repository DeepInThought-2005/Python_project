import tkinter as tk


WIN_WIDTH = 400
WIN_HEIGHT = WIN_WIDTH//80*100
W = 'white'
B = 'black'
BLACK_WINS = ("Congratulations!", "Black won!")
WHITE_WINS = ("Congratulations!", "White won!")
DRAW = ("Great fight!", "Draw...")
ZUGZWANG_WHITE = ("Oops!", "No more valid moves for Black, but White has!")
ZUGZWANG_BLACK = ("Oops!", "No more valid moves for White, but Black has!")
EDIT_MODE = 'edit'
HUMAN_AI = 'HUMAN-AI'
HUMAN_HUMAN = 'HUMAN-HUMAN'
AI_AI = 'AI-AI'
BG_COLOR = '#302E2B'
CAPTURABLE = 'capturable' # valid move draw style
EVAL = 'evaluation' # valid move draw style
DOT = 'dot' # valid move draw style
INVIS = 'invisible' # valid move draw style
EMPTY = -1
INF = 999999
CALCULATING = 'calculating' # for main.py sidecanvas


# Weight table for the board positions
'''
WEIGHT_TABLE = [
    [100, -20, 10,  5,  5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10,  -2,  5,  1,  1,  5,  -2,  10],
    [5,   -2,  1,  1,  1,  1,  -2,   5],
    [5,   -2,  1,  1,  1,  1,  -2,   5],
    [10,  -2,  5,  1,  1,  5,  -2,  10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10,  5,  5, 10, -20, 100]
]
'''

def generate_weight_table(rows=8, cols=8):
    if rows == 8 and cols == 8: # University of washington respresents
        weight_board = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
    ]
    else:
        weight_board = [[0] * cols for _ in range(rows)]

        # Assign weights
        for row in range(rows):
            for col in range(cols):
                if (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1):
                    weight_board[row][col] = 20  # Corners
                elif (row == 0 or row == rows - 1) and (col == 1 or col == cols - 2):
                    weight_board[row][col] = -3  # Adjacent to corners on edges
                elif (row == 1 or row == rows - 2) and (col == 0 or col == cols - 1):
                    weight_board[row][col] = -3  # Adjacent to corners on edges
                elif (row == 0 or row == rows - 1) or (col == 0 or col == cols - 1):
                    weight_board[row][col] = 8  # Other edge positions
                elif (row == 1 or row == rows - 2) and (col == 1 or col == cols - 2):
                    weight_board[row][col] = -7  # Adjacent to edges but not corners
                else:
                    weight_board[row][col] = 2  # Center and other positions

    return weight_board


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(WIN_WIDTH)+"x"+str(WIN_HEIGHT))
        self.configure(bg=BG_COLOR)
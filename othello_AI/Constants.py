import tkinter as tk


WIN_WIDTH = 400
WIN_HEIGHT = WIN_WIDTH//80*100
W = 'white'
B = 'black'
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
def generate_weight_board(rows=8, cols=8):
    weight_board = [[0] * cols for _ in range(rows)]

    # Assign weights
    for row in range(rows):
        for col in range(cols):
            if (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1):
                weight_board[row][col] = 100  # Corners
            elif (row == 0 or row == rows - 1) and (col == 1 or col == cols - 2):
                weight_board[row][col] = -20  # Adjacent to corners on edges
            elif (row == 1 or row == rows - 2) and (col == 0 or col == cols - 1):
                weight_board[row][col] = -20  # Adjacent to corners on edges
            elif (row == 0 or row == rows - 1) or (col == 0 or col == cols - 1):
                weight_board[row][col] = 10  # Other edge positions
            elif (row == 1 or row == rows - 2) and (col == 1 or col == cols - 2):
                weight_board[row][col] = 5  # Adjacent to edges but not corners
            else:
                weight_board[row][col] = 1  # Center and other positions

    return weight_board


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(WIN_WIDTH)+"x"+str(WIN_HEIGHT))
        self.configure(bg=BG_COLOR)
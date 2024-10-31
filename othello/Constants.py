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
NUMBER = 'number' # valid move draw style
DOT = 'dot' # valid move draw style
EMPTY = 0



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(str(WIN_WIDTH)+"x"+str(WIN_HEIGHT))
        self.configure(bg=BG_COLOR)
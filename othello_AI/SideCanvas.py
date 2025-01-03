import tkinter as tk
from Constants import *

class UpperCanvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root)
        self.r = root    
        self.restart = tk.Button(self, text="restart")

        self.w_counter = tk.Label(self, text="White: 2", font=("Helvetica", 25), bg=BG_COLOR, fg="lightgray")
        self.b_counter = tk.Label(self, text="Black: 2", font=("Helvetica", 25), bg=BG_COLOR, fg="lightgray")

        self.configure(bg=BG_COLOR, highlightbackground=BG_COLOR)

        self.bind("<Configure>", self.size_update)
    
    def pack_self(self):
        # self.restart.pack(side='left', padx=10)
        # self.w_count.pack(side='left', padx=5)
        self.w_counter.pack(expand=True, side='left')
        self.b_counter.pack(expand=True, side='right')
        self.pack(expand=True, fill="both")

    def size_update(self, event):
        self.delete(tk.ALL)
        size = min(self.r.winfo_height(), self.r.winfo_width()) // 20
        self.w_counter['font'] = ("Helvetica", size)
        self.b_counter['font'] = ("Helvetica", size)

    
    def draw_pieces_left(self, n, col, row):
        w = self.winfo_width()
        for i in range(n):
            self.create_line(w/10*1+(i+1)*(w/10*8/(col*row/2)),
                             self.winfo_height()/10*1,
                             w/10*1+(i+1)*(w/10*8/(col*row/2)),
                             self.winfo_height()/10*9)
            self.create_rectangle(w/10*1+i*(w/10*8/(col*row/2)),
                                  self.winfo_height()/10*1,
                                  w/10*1+(i+0.5)*(w/10*8/(col*row/2)),
                                  self.winfo_height()/10*9,
                                  fill='black')
        

class UnderCanvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root)
        self.r = root

        self.hint = tk.Label(self, text="Black to move...", font=("Helvetica", 25), bg=BG_COLOR, fg='lightgray')

        self.configure(bg=BG_COLOR, highlightbackground=BG_COLOR)

        self.bind("<Configure>", self.size_update)

    def pack_self(self):
        self.hint.pack(expand=True)
        
        self.pack(expand=True, fill="both")
    
    def size_update(self, event):
        self.delete(tk.ALL)
        size = min(self.r.winfo_height(), self.r.winfo_width()) // 20
        self.hint['font'] = ("Helvetica", size)

        # draw pieces holding rectangle
        # self.create_rectangle(self.winfo_width()/10*1,
        #                       self.winfo_height()/10*1,
        #                       self.winfo_width()/10*9,
        #                       self.winfo_height()/10*9,
        #                       width=2)


class LeftCanvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root)
        self.r = root
        self.piece_left = tk.Label(self, text="Hi")
    
    def pack_self(self):
        self.piece_left.pack()
        self.place(x=0, y=WIN_HEIGHT//8*2)

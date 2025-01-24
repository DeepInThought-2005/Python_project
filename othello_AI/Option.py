import tkinter as tk
from Constants import *

class Option(tk.Canvas):
    def __init__(self, root:App, boardCanvas) -> None:
        super().__init__(root)
        self.bind("<Configure>", self._update)
        self.r = root
        self.board = boardCanvas

        self.row_column_list = (4, 6, 8, 10 ,12, 14, 16)
        self.on_off = ("on", "off")
        self.show_vm_as = (CAPTURABLE, DOT, INVIS)
        self.mode = ("HUMAN-HUMAN", "HUMAN-AI")
        self.depth = (1, 2, 3, 4, 5, 6)
        self.it_limit = (1000, 2000, 5000, 10000, 20000, 50000, "Infinite")

        self.row = 0
        self.col = 0

        # Row and Col list
        self.rowcolVar = tk.IntVar()
        self.rowcolVar.set(self.board.row)
        self.rowcol_f = tk.Frame(self)
        self.rowcol_l = tk.Label(self.rowcol_f, text="Board size: ")
        self.rowcol_l.grid(column=0, row=0, sticky = tk.E)
        self.rowcol_o = tk.OptionMenu(self.rowcol_f, self.rowcolVar, *self.row_column_list)
        self.rowcol_o.grid(column=1, row=0, sticky = tk.W)


        # show_valid_move
        self.ShowVmVar = tk.StringVar() 
        self.ShowVmVar.set(CAPTURABLE)
        self.is_show_vm_f = tk.Frame(self)
        self.is_show_vm_l = tk.Label(self.is_show_vm_f, text="Show valid move as: ")
        self.is_show_vm_l.grid(column=0, row=0, sticky = tk.E)
        self.is_show_vm_o = tk.OptionMenu(self.is_show_vm_f, self.ShowVmVar, *self.show_vm_as)
        self.is_show_vm_o.grid(column=1, row=0, sticky = tk.W)

        # is_animating
        self.isAnimeVar = tk.StringVar() 
        self.isAnimeVar.set("on")
        self.is_anime_f = tk.Frame(self)
        self.is_anime_l = tk.Label(self.is_anime_f, text="Animating flip: ")
        self.is_anime_l.grid(column=0, row=0, sticky = tk.E)
        self.is_anime_o = tk.OptionMenu(self.is_anime_f, self.isAnimeVar, *self.on_off)
        self.is_anime_o.grid(column=1, row=0, sticky = tk.W)

        # mode
        self.modeVar = tk.StringVar()
        self.modeVar.set("HUMAN-HUMAN")
        self.mode_f = tk.Frame(self)
        self.mode_l = tk.Label(self.mode_f, text="Game mode: ")
        self.mode_l.grid(column=0, row=0, sticky = tk.E)
        self.mode_o = tk.OptionMenu(self.mode_f, self.modeVar, *self.mode)
        self.mode_o.grid(column=1, row=0, sticky = tk.W)

        # AI_depth
        self.depthVar = tk.IntVar() 
        self.depthVar.set(3)
        self.depth_f = tk.Frame(self)
        self.depth_l = tk.Label(self.depth_f, text="Algorithm depth: ")
        self.depth_l.grid(column=0, row=0, sticky = tk.E)
        self.depth_o = tk.OptionMenu(self.depth_f, self.depthVar, *self.depth)
        self.depth_o.grid(column=1, row=0, sticky = tk.W)

        # iteration_limit
        self.it_limitVar = tk.StringVar()
        self.it_limitVar.set(10000)
        self.it_limit_f = tk.Frame(self)
        self.it_limit_l = tk.Label(self.it_limit_f, text="Iteration limit: ")
        self.it_limit_l.grid(column=0, row=0, sticky = tk.E)
        self.it_limit_o = tk.OptionMenu(self.it_limit_f, self.it_limitVar, *self.it_limit)
        self.it_limit_o.grid(column=1, row=0, sticky = tk.W)


        self.cancel_b = tk.Button(self, text="Cancel")
        self.save_b = tk.Button(self, text="Save")

        self.grid_all()

    def grid_all(self):
        # self.row_f.pack(column=0, row=0, sticky="w", padx=10, pady=10)
        # self.col_f.pack(column=1, row=0, sticky="e", padx=10, pady=10)
        # self.is_show_eval_f.pack(column=0, row=1, sticky="w", padx=10, pady=10)
        # self.is_show_vm_f.pack(column=1, row=1, sticky="e", padx=10, pady=10)
        # self.mode_f.pack(column=0, row=2, sticky="w", padx=10, pady=10)
        # self.depth_f.pack(column=1, row=2, sticky="e", padx=10, pady=10)
        # self.cancel_b.pack(column=0, row=3, sticky="w", padx=10, pady=10)
        # self.save_b.pack(column=1, row=3, sticky="e", padx=10, pady=10)

        self.rowcol_f.pack(pady=10)
        # self.is_show_eval_f.pack(pady=10)
        self.is_show_vm_f.pack(pady=10)
        self.is_anime_f.pack(pady=10)
        self.mode_f.pack(pady=10)
        self.depth_f.pack(pady=10)
        self.it_limit_f.pack(pady=10)
        self.cancel_b.pack(pady=10)
        self.save_b.pack(pady=10)

    
    def _update(self, event):
        # w = self.r.winfo_width()
        self.configure(width=self.r.winfo_width(), height=self.r.winfo_height())
        # if w-2*self.row_f.winfo_width() > 0:
        #     self.col_f.grid_configure(padx=w-2*self.row_f.winfo_width())
        #     self.save_b.grid_configure(padx=w-2*self.row_f.winfo_width())
        # self.row_f.grid_configure(padx=w//2.6-self.row_f.winfo_width(), pady=self.winfo_height()//10)
        # self.is_show_eval_f.grid_configure(pady=self.row_f.winfo_height())
        # self.col_f.grid_configure(padx=w//4)

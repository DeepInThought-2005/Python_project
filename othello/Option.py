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
        self.mode = ("HUMAN-HUMAN", "HUMAN-AI", "AI-AI")
        self.depth = (1, 2, 3, 4, 5, 6)

        self.row = 0
        self.col = 0

        # Row list
        self.rowVar = tk.IntVar()
        self.rowVar.set(self.board.row)
        self.row_f = tk.Frame(self)
        self.row_l = tk.Label(self.row_f, text="Rows: ")
        self.row_l.grid(column=0, row=0, sticky = tk.E)
        self.row_o = tk.OptionMenu(self.row_f, self.rowVar, *self.row_column_list)
        self.row_o.grid(column=1, row=0, sticky = tk.W)

        # Col list
        self.colVar = tk.IntVar()
        self.colVar.set(self.board.col)
        self.col_f = tk.Frame(self)
        self.col_l = tk.Label(self.col_f, text="Columns: ")
        self.col_l.grid(column=0, row=0, sticky = tk.E)
        self.col_o = tk.OptionMenu(self.col_f, self.colVar, *self.row_column_list)
        self.col_o.grid(column=1, row=0, sticky = tk.W)

        # Show evaluation list
        self.validStyleVar = tk.StringVar()
        self.validStyleVar.set("on")
        self.is_show_eval_f = tk.Frame(self)
        self.is_show_eval_l = tk.Label(self.is_show_eval_f, text="Show evalution: ")
        self.is_show_eval_l.grid(column=0, row=0, sticky = tk.E)
        self.is_show_eval_o = tk.OptionMenu(self.is_show_eval_f, self.validStyleVar, *self.on_off)
        self.is_show_eval_o.grid(column=1, row=0, sticky = tk.W)

        # is_show_valid_move
        self.isVmVar = tk.StringVar() # is show valid move?
        self.isVmVar.set("on")
        self.is_show_vm_f = tk.Frame(self)
        self.is_show_vm_l = tk.Label(self.is_show_vm_f, text="Show valid move: ")
        self.is_show_vm_l.grid(column=0, row=0, sticky = tk.E)
        self.is_show_vm_o = tk.OptionMenu(self.is_show_vm_f, self.isVmVar, *self.on_off)
        self.is_show_vm_o.grid(column=1, row=0, sticky = tk.W)

        # mode
        self.modeVar = tk.StringVar() # is show valid move?
        self.modeVar.set("HUMAN-HUMAN")
        self.mode_f = tk.Frame(self)
        self.mode_l = tk.Label(self.mode_f, text="Game mode: ")
        self.mode_l.grid(column=0, row=0, sticky = tk.E)
        self.mode_o = tk.OptionMenu(self.mode_f, self.modeVar, *self.mode)
        self.mode_o.grid(column=1, row=0, sticky = tk.W)

        # AI_depth
        self.depthVar = tk.IntVar() # is show valid move?
        self.depthVar.set(3)
        self.depth_f = tk.Frame(self)
        self.depth_l = tk.Label(self.depth_f, text="Algorithm depth: ")
        self.depth_l.grid(column=0, row=0, sticky = tk.E)
        self.depth_o = tk.OptionMenu(self.depth_f, self.depthVar, *self.depth)
        self.depth_o.grid(column=1, row=0, sticky = tk.W)


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

        self.row_f.pack(pady=10)
        self.col_f.pack(pady=10)
        self.is_show_eval_f.pack(pady=10)
        self.is_show_vm_f.pack(pady=10)
        self.mode_f.pack(pady=10)
        self.depth_f.pack(pady=10)
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

import tkinter as tk
from tkinter import ttk

from SideCanvas import *
from Constants import *
from Board import *
from Option import *


app = App()


class Bootstrap():
    def __init__(self, app:App):
        self.r = app
        self.r.title("Othello - not for noobs!")
        self.mode = EDIT_MODE
        self.bC = BoardCanvas(app)
        self.upC = UpperCanvas(app)
        self.unC = UnderCanvas(app)
        self.lC = LeftCanvas(app)

        self.options = Option(app, self.bC)

        self.menubar = tk.Menu(self.r)
        self.r.config(menu=self.menubar)
        self.game_menu = tk.Menu(self.menubar, tearoff=0, cursor="hand2",
                                 selectcolor="red")
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        
        self.menubar.add_cascade(label="game", menu=self.game_menu)

        self.menubar.add_command(label="options", command=self.option_onclick)

        self.game_menu.add_command(label="new game", command=lambda: self.bC.init_board(self.bC.col, self.bC.row))
        self.game_menu.add_command(label="undo (Ctrl+Z)", command=self.bC.undo)
        self.game_menu.add_command(label="redo (Ctrl+Y)", command=self.bC.redo)
        self.game_menu.add_command(label="AI move (Ctrl+A)", command=self.bC.AI_move)

        self.pack_all()
        self.r.bind("<Configure>", self._update)
        self.r.bind("<Button-1>", self.app_clicked)
        self.r.bind("<Control-z>", self.undo)
        self.r.bind("<Control-y>", self.redo)
        self.r.bind("<Control-a>", self.AI_move)

        # self.bC.get_move_scores(B, 3)
        # self.bC.print_board()
        
    def option_onclick(self):
        self.upC.pack_forget()
        self.bC.pack_forget()
        self.unC.pack_forget()

        def on_close():
            self.options.pack_forget()
            self.pack_all()
    
        def on_save():
            t_col = self.bC.col
            self.bC.col = self.options.colVar.get()
            t_row = self.bC.row
            self.bC.row = self.options.rowVar.get()
            self.bC.weight_table = generate_weight_board(self.bC.col, self.bC.row)
            self.bC.show_vm_as = self.options.ShowVmVar.get()
            if self.options.ShowVmVar.get() == INVIS:
                self.bC.is_draw_valid_moves = False

            if self.options.isAnimeVar.get() == 'on':
                self.bC.is_animating_flip = True
            elif self.options.isAnimeVar.get() == 'off':
                self.bC.is_animating_flip = False

            self.bC.mode = self.options.modeVar.get()
            self.bC.depth = self.options.depthVar.get()
        
            self.options.pack_forget()
            self.pack_all()
            if t_col != self.bC.col or t_row != self.bC.row:
                self.bC.init_board(self.bC.col, self.bC.row)
            self._update(None)

        self.options.cancel_b.configure(command=on_close)
        self.options.save_b.configure(command=on_save)

        self.options.pack(expand=True, fill="both")



    def pack_all(self):
        self.upC.pack_self()
        # self.lC.pack_self()
        self.bC.pack_self()
        self.unC.pack_self()

    def set_mode(self):
        if self.bC.mode == HUMAN_AI:
            if self.bC.play_as == W:
                if self.bC.turn == W:
                    self.unC.hint['text'] = "Your move..."
                else:
                    self.unC.hint['text'] = "Computer is thinking..."

        elif self.bC.mode == HUMAN_HUMAN:
            if self.bC.play_as == W:
                if self.bC.turn == W:
                    self.unC.hint['text'] = "Player 1 to move..."
                else:
                    self.unC.hint['text'] = "Player 2 to move..."
        
    def edit_mode(self):
        pass

    def update_side_canvas(self):
        self.upC.b_counter['text'] = "White: " + str(self.bC.get_pieces_left(B))
        self.upC.w_counter['text'] = "White: " + str(self.bC.get_pieces_left(W))
        if self.bC.turn == B:
            self.unC.hint['text'] = "Black to move..."
        else:
            self.unC.hint['text'] = "White to move..."

    def AI_move(self, event=None):
        self.bC.AI_move()
        self.update_side_canvas()

    def undo(self, event=None):
        self.bC.undo()
        self.update_side_canvas()

    def redo(self, event=None):
        self.bC.redo()
        self.update_side_canvas()

    def app_clicked(self, event):
        if not self.bC.animating:
            self.bC.clicked(event)
            self.set_mode()

            self.upC.w_counter['text'] = "White: " + str(self.bC.get_pieces_left(W))
            self.upC.b_counter['text'] = "White: " + str(self.bC.get_pieces_left(W))
            self.update_side_canvas()
            if self.bC.game_state:
                messagebox.showinfo(self.bC.game_state[0], self.bC.game_state[1])
                self.bC.game_state = ""


    def _update(self, event):
        if self.r.winfo_height() > self.r.winfo_width():
            self.bC.configure(height=self.r.winfo_width()//8*6)
        elif self.r.winfo_height() < self.r.winfo_width():
            self.bC.configure(height=self.r.winfo_height()//8*6)
        self.bC.configure(width=self.bC.winfo_height())
        # self.upC.configure(width=self.bC.winfo_width(), height=self.bC.winfo_height()//8)
        # self.unC.configure(width=self.bC.winfo_width(), height=self.bC.winfo_height()//8)
        self.upC.size_update(event)
        self.unC.size_update(event)

        self.upC.w_counter['text'] = "White: " + str(self.bC.get_pieces_left(W))
        self.upC.b_counter['text'] = "Black: " + str(self.bC.get_pieces_left(B))

        self.set_mode()
        self.bC.redraw()
        # self.unC.draw_pieces_left(self.bC.pieces_left[B], self.bC.col, self.bC.row)
        # self.upC.draw_pieces_left(self.bC.pieces_left[W], self.bC.col, self.bC.row)
            

if __name__ == "__main__":
    Bootstrap(app)
    app.mainloop()
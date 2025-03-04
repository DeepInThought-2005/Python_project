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
        self.r.title("Othello - noobs better stay away!")
        self.mode = EDIT_MODE
        self.is_in_option_menu = False
        self.iteration_limit = 10000
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
        self.game_menu.add_command(label="AI move (Ctrl+A)", command=self.AI_move)

        self.pack_all()
        self.r.bind("<Configure>", self._update)
        self.r.bind("<Button-1>", self.app_clicked)
        self.r.bind("<Control-z>", self.undo)
        self.r.bind("<Control-y>", self.redo)
        self.r.bind("<Control-a>", self.AI_move)

        # self.bC.get_move_scores(B, 3)
        # self.bC.print_board()
        self.reset_eval_list()
        self.bC.redraw()
        self.update_side_canvas()
        
    def option_onclick(self):
        self.is_in_option_menu = True
        self.upC.pack_forget()
        self.bC.pack_forget()
        self.unC.pack_forget()

        def on_close():
            self.options.pack_forget()
            self.pack_all()
            self.is_in_option_menu = False
    
        def on_save():
            self.options.pack_forget()
            self.pack_all()
            t_col = self.bC.col
            self.bC.col = self.options.rowcolVar.get()
            t_row = self.bC.row
            self.bC.row = self.options.rowcolVar.get()
            if t_col != self.bC.col or t_row != self.bC.row:
                self.bC.init_board(self.bC.col, self.bC.row)
                self.bC.weight_table = generate_weight_table(self.bC.col, self.bC.row)
            self._update(None)
            self.bC.show_vm_as = self.options.ShowVmVar.get()

            if self.options.ShowVmVar.get() == INVIS:
                self.bC.is_draw_valid_moves = False

            if self.options.isAnimeVar.get() == 'on':
                self.bC.is_animating_flip = True
            elif self.options.isAnimeVar.get() == 'off':
                self.bC.is_animating_flip = False

            self.bC.mode = self.options.modeVar.get()
            self.bC.depth = self.options.depthVar.get()

            it_limit = self.options.it_limitVar.get()
            if it_limit == "Infinite":
                self.iteration_limit = INF
            else:
                self.iteration_limit = int(it_limit)


            self.bC.redraw()
            if self.bC.show_vm_as == EVAL:
                self.reset_eval_list()
            self.is_in_option_menu = False
        


        self.options.cancel_b.configure(command=on_close)
        self.options.save_b.configure(command=on_save)

        self.options.pack(expand=True, fill="both")



    def pack_all(self):
        self.upC.pack_self()
        # self.lC.pack_self()
        self.bC.pack_self()
        self.unC.pack_self()
        
    def edit_mode(self):
        pass

    def update_side_canvas(self):
        self.upC.b_counter['text'] = "Black: " + str(self.bC.get_pieces_left(self.bC.array, B))
        self.upC.w_counter['text'] = "White: " + str(self.bC.get_pieces_left(self.bC.array, W))
        if not self.bC.calculating:
            if self.bC.turn == B:
                self.unC.hint['text'] = "Black to move..."
            else:
                self.unC.hint['text'] = "White to move..."

    def AI_move(self, event=None):
        if not self.bC.animating and not self.bC.calculating:
            self.reset_eval_list()
            self.bC.AI_move()
            self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
            self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)
            if self.bC.show_vm_as == EVAL:
                self.reset_eval_list()

            if not self.bC.valid_moves:
                self.bC.switch_turn()
                self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)
                if not self.bC.valid_moves:
                    self.update_side_canvas()
                    self.bC.redraw()
                    messagebox.showinfo("Game ends", self.get_game_state())
            self.bC.redraw()
            self.bC.update()
            self.bC.print_board(self.bC.array)

            self.update_side_canvas()

    def undo(self, event=None):
        if not self.bC.calculating and not self.bC.animating:
            self.bC.undo()
            self.update_side_canvas()

    def redo(self, event=None):
        if not self.bC.calculating and not self.bC.animating:
            self.bC.redo()
            self.update_side_canvas()

    def app_clicked(self, event):
        if not self.bC.animating and not self.bC.calculating and not self.is_in_option_menu:
            if(self.bC.clicked(event)):                          
                self.bC.switch_turn()
                self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)
                self.bC.redraw()

                if not self.bC.valid_moves and self.bC.mode != HUMAN_AI:
                    self.bC.switch_turn()
                    self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                    self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)
                    if not self.bC.valid_moves:
                        self.update_side_canvas()
                        self.bC.redraw()
                        messagebox.showinfo("Game ends", self.get_game_state())


                if self.bC.show_vm_as == EVAL:
                    self.update_side_canvas()
                    self.reset_eval_list()
                    self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                    self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)
                    self.bC.redraw()

                if self.bC.mode == HUMAN_AI:
                    if(self.bC.get_valid_moves(self.bC.array, self.bC.turn)):
                        self.update_side_canvas()
                        temp = True
                        while(temp):
                            self.reset_eval_list()
                            if(self.bC.AI_move()):
                                self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                                self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)

                                if not self.bC.valid_moves:
                                    self.bC.switch_turn()
                                    self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                                    self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)
                                    if not self.bC.valid_moves:
                                        self.update_side_canvas()
                                        self.bC.redraw()
                                        messagebox.showinfo("Game ends", self.get_game_state())
                                        temp = False
                                else:
                                    temp = False
                            else:
                                temp = False

                        self.bC.redraw()
                        self.bC.update()
                        self.bC.print_board(self.bC.array)
                    else:
                        self.bC.switch_turn()
                        self.bC.valid_moves = self.bC.get_valid_moves(self.bC.array, self.bC.turn)
                        self.bC.capturable_list = self.bC.get_capturable(self.bC.array, self.bC.turn, self.bC.valid_moves)

                        if not self.bC.valid_moves:
                            self.update_side_canvas()
                            self.bC.redraw()
                            messagebox.showinfo("Game ends", self.get_game_state())
                        self.bC.redraw()
                        self.bC.update()
                        self.bC.print_board(self.bC.array)

            
            self.update_side_canvas()


    def get_game_state(self):
        msg = ""
        if self.bC.get_pieces_left(self.bC.array, B) > self.bC.get_pieces_left(self.bC.array, W):
            msg = "Black wins!"
        elif self.bC.get_pieces_left(self.bC.array, B) < self.bC.get_pieces_left(self.bC.array, W):
            msg = "White wins!"
        else:
            msg = "Draw!"
        
        return msg

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

        self.update_side_canvas()

        self.bC.redraw()
        # self.unC.draw_pieces_left(self.bC.pieces_left[B], self.bC.col, self.bC.row)
        # self.upC.draw_pieces_left(self.bC.pieces_left[W], self.bC.col, self.bC.row)

    def minimax(self, board, depth, maximizing_player, turn, alpha, beta, iteration_limit):
        self.bC.counter+=1
        self.unC.hint['text'] = "Calculated " + str(self.bC.counter) + " positions..."
        self.unC.update()

        if self.bC.counter >= iteration_limit:
            return self.bC.evaluate(board, turn), []

        if turn == W:
            opponent = B
        else:
            opponent = W
        if maximizing_player:
            valid_moves = self.bC.get_valid_moves(board, turn)
        else:
            valid_moves = self.bC.get_valid_moves(board, opponent)
        
        if depth == 0 or not valid_moves:
            return self.bC.evaluate(board, turn), []
        
        move_evaluations = {}
        
        if maximizing_player:
            max_eval = -INF
            for move in valid_moves:
                new_board = self.bC.apply_move([row[:] for row in board], move[0], move[1], turn)
                eval, _ = self.minimax(new_board, depth - 1, False, turn, alpha, beta, self.iteration_limit)
                move_evaluations[move] = eval
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, move_evaluations
        else:
            min_eval = INF
            for move in valid_moves:
                new_board = self.bC.apply_move([row[:] for row in board], move[0], move[1], opponent)
                eval, _ = self.minimax(new_board, depth - 1, True, turn, alpha, beta, self.iteration_limit)
                move_evaluations[move] = eval
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, move_evaluations
    
        
    def reset_eval_list(self):
        self.bC.calculating = True
        self.bC.update()
        self.bC.counter = 0
        self.bC.eval_list = self.minimax(self.bC.array, self.bC.depth, True, self.bC.turn, -INF, INF, self.iteration_limit)[1]
        print(self.bC.eval_list)
        # self.update()
        self.bC.calculating = False
            

if __name__ == "__main__":
    Bootstrap(app)
    app.mainloop()
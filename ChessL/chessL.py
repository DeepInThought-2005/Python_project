import pygame
from pygame.constants import VIDEORESIZE
from constants import *
from board import *
from control import *

def draw_window(win, control, w, h):
    control.board.resize(w, h)
    win.blit(control.board.board_img, (0, 0))
    control.board.draw_valid_moves(win, control.valid_moves, control.turn, w // 8, h // 8)
    # draw mark
    for i in range(8):
        for j in range(8):
            if control.marked_pos[i][j] == 1:
                control.draw_color(win, hell_red, red, (i, j), w // 8, h // 8)
    # draw selected
    if control.selected_pos:
        pygame.draw.rect(win, select_color, (control.selected_pos[0] * w // 8, control.selected_pos[1] * h // 8, w // 8, h // 8))
    control.board.resize_pieces(w, h)
    control.board.draw_pieces(win)
    # solve the layer problem!
    if control.selected_pos:
        control.board.board[control.selected_pos[0]][control.selected_pos[1]].draw(win)
    

    pygame.display.update()


def get_square_onclick(m_x, m_y, w, h):
    for j in range(8):
        for i in range(8):
            if m_x >= i * w and m_x <= i * w + w and m_y >= j * h and m_y <= j * h + h:
                return i, j


def main():
    def todo_after_move():
        control.valid_moves = []
        control.board.set_every_coord()
        control.board.set_every_pos()
        control.selected_pos = ()
        control.board.unselectall()
    win = pygame.display.set_mode((DEF_WIDTH, DEF_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("ChessL")
    board = Board()
    control = Control(board)
    win_width = 0
    win_height = 0
    clock = pygame.time.Clock()
    selected = False
    run = True
    while run:
        win_width = win.get_width()
        win_height = win.get_height()
        draw_window(win, control, win_width, win_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.VIDEORESIZE:
                control.board.set_every_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = event.pos
                if m_x < win_width:
                    x, y = control.get_onclick(m_x, m_y)
                    if pygame.mouse.get_pressed()[0]:
                        control.marked_pos = [[0] * 8 for _ in range(8)]
                        if x != -1:
                            selected = True
                            control.selected_pos = (x, y)
                            control.board.board[x][y].selected = True
                            if control.turn == control.board.board[x][y].color:
                                control.get_valid_moves(x, y)
                                

                    x, y = get_square_onclick(m_x, m_y, win_width // 8, win_height // 8)
                    if pygame.mouse.get_pressed()[2]:
                        if m_x < win_width:
                            control.mark((x, y))

            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = event.pos
                selected = False
                if m_x < win_width:
                    x, y = get_square_onclick(m_x, m_y, win_width // 8, win_height // 8)
                    if control.selected_pos:

                        tx, ty = control.selected_pos
                        bo = control.board.board
                        start = bo[tx][ty]
                        if bo[tx][ty] != 0:
                            if (tx, ty) != (x, y):
                                if (x, y) in control.valid_moves:
                                    control.make_move((tx, ty), (x, y))
                                    control.change_turn()
                                else:
                                    control.board.board[tx][ty] = start
                            else:
                                control.board.board[tx][ty] = start
                        else:
                            control.board.board[tx][ty] = start
                    control.board.set_every_pos()



                    # check game result
                    control.change_turn()
                    result = control.check_gameover(control.turn)
                    if result == CHECKMATE:
                        control.game_over(win)
                        control.gameover = True
                    elif result == STALEMATE:
                        control.game_over(win, stalemate=True)
                        control.gameover = True
                    elif result == DRAW:
                        control.game_over(win, tie=True)
                        control.gameover = True

                    control.change_turn()

                else:
                    if control.selected_pos:
                        print(x, y, control.selected_pos)
                        control.board.board[x][y].change_pos((x, y))
                if event.type != VIDEORESIZE:
                    todo_after_move()
                    draw_window(win, control, win_width, win_height)
        
            if event.type == pygame.MOUSEMOTION:
                m_x, m_y = event.pos
                if selected:
                    bo = control.board.board
                    if m_x > win_width:
                        m_x = win_width
                    img_x = m_x - win_width // 8 / 2
                    img_y = m_y - win_height // 8 / 2
                    for j in range(8):
                        for i in range(8):
                            if bo[i][j] != 0:
                                if bo[i][j].selected:
                                    control.board.board[i][j].x = img_x
                                    control.board.board[i][j].y = img_y

        
        clock.tick(60)


main()

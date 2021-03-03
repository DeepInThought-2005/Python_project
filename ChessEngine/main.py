import pygame
from constants import *
import time
import copy
import random
from board import *
pygame.mixer.init()
pygame.font.init()

a_cool_position = "5B1k/1R6/5p1K/1n1r3p/8/8/8/5b2 w"

# AI part
def evaluate(board, max_color):
    if max_color == WHITE:
        return board.white_score - board.black_score
    else:
        return board.black_score - board.white_score


def minimax(board, depth, max_turn, max_color):
    if depth == 0 or board.game_over():
        return None, evaluate(board, max_color)
    moves = board.get_valid_moves(max_turn)
    best_move = random.choice(moves)



def draw_window(win, board, valid_moves, turn, marked_pos, black_time, white_time, last_move, move_text=""):
    win.fill(hell_green)
    t1 = black_time
    t2 = white_time
    formattime1 = str(t1 // 60) + ':' + str(t1 % 60)
    formattime2 = str(t2 // 60) + ':' + str(t2 % 60)

    if t1 % 60 == 0:
        formattime1 = str(t1 // 60) + ':' + '00'
    if t2 % 60 == 0:
        formattime2 = str(t2 // 60) + ':' + '00'

    if t1 % 60 < 10:
        formattime1 = str(t1 // 60) + ':' + '0' + str(t1 % 60)
    if t2 % 60 < 10:
        formattime2 = str(t2 // 60) + ':' + '0' + str(t2 % 60)

    font1 = pygame.font.SysFont("times", 50)
    font2 = pygame.font.SysFont("Arial", 45)
    text1 = font2.render("Time: " + str(formattime1), 1, black)
    text2 = font2.render("Time: " + str(formattime2), 1, black)
    win.blit(text2, (WIDTH + 300 // 2 - text1.get_width() // 2, HEIGHT - 50 - text2.get_height() // 2))
    win.blit(text1, (WIDTH + 300 // 2 - text1.get_width() // 2, 10 + text1.get_height()))
    move_txt = font1.render(move_text, 1, black)
    win.blit(move_txt, (WIDTH + 300 // 2 - move_txt.get_width() // 2, HEIGHT // 2 - move_txt.get_height() // 2))


    board.draw(win)

    if last_move:
        start = last_move[0]
        end = last_move[1]
        if start[0] % 2 == 0:
            if start[1] % 2 != 0:
                pygame.draw.rect(win, dark_orange, (start[0] * W, start[1] * W, W, W))
            if start[1] % 2 == 0:
                pygame.draw.rect(win, hell_orange, (start[0] * W, start[1] * W, W, W))
        else:
            if start[1] % 2 == 0:
                pygame.draw.rect(win, dark_orange, (start[0] * W, start[1] * W, W, W))
            if start[1] % 2 != 0:
                pygame.draw.rect(win, hell_orange, (start[0] * W, start[1] * W, W, W))

        if end[0] % 2 == 0:
            if end[1] % 2 != 0:
                pygame.draw.rect(win, dark_orange, (end[0] * W, end[1] * W, W, W))
            if end[1] % 2 == 0:
                pygame.draw.rect(win, hell_orange, (end[0] * W, end[1] * W, W, W))
        else:
            if end[1] % 2 == 0:
                pygame.draw.rect(win, dark_orange, (end[0] * W, end[1] * W, W, W))
            if end[1] % 2 != 0:
                pygame.draw.rect(win, hell_orange, (end[0] * W, end[1] * W, W, W))


    board.draw_valid_moves(win, valid_moves, board.board, turn)
    king_pos = board.get_king_pos(change_turn(turn))


    # draw mark
    for i in range(8):
        for j in range(8):
            if marked_pos[i][j] == 1:
                color = ()
                if i % 2 == 0:
                    if j % 2 != 0:
                        color = dark_red
                    if j % 2 == 0:
                        color = hell_red
                else:
                    if j % 2 == 0:
                        color = dark_red
                    if j % 2 != 0:
                        color = hell_red
                pygame.draw.rect(win, color, (i * W, j * W, W, W))
    m_x = pygame.mouse.get_pos()[0]
    if m_x < WIDTH:
        if board.check(change_turn(turn)):
            pygame.draw.rect(win, checked, (king_pos[0] * W, king_pos[1] * W, W, W))

    # Two times for loop to solve the layer problem!
    for i in range(8):
        for j in range(8):
            if board.board[i][j] != 0:
                if turn != board.board[i][j].color:
                    board.board[i][j].draw(win)

    for i in range(8):
        for j in range(8):
            if board.board[i][j] != 0:
                if turn == board.board[i][j].color:
                    board.board[i][j].draw(win)

    pygame.display.update()

def get_pos(m_x, m_y):
    for i in range(8):
        for j in range(8):
            if m_x >= j * W and m_x <= j * W + W and m_y >= i * W and m_y <= i * W + W:
                return j, i

def change_turn(turn):
    if turn == BLACK:
        turn = WHITE
    else:
        turn = BLACK
    return turn


def onclick(x, y, m_x, m_y):
    if m_x > x and m_x < x + W and m_y > y and m_y < y + W:
        return True
    return False


def game_over(win, turn, board, tie=False):
    START_END.play()
    turn = change_turn(turn)
    # win.fill(black)
    board.set_every_pos()
    # board.set_every_coord()
    board.unselectall()

    # draw the board again
    board.draw(win)
    for i in range(8):
        for j in range(8):
            if board.board[i][j] != 0:
                board.board[i][j].draw(win)

    text_font = pygame.font.SysFont("times", 100)
    hint_font = pygame.font.SysFont("times", 60)
    if tie:
        text = text_font.render("Draw!", 1, red)
    else:
        text = text_font.render(turn + ' checkmates!', 1, red)
    hint = hint_font.render("click anywhere to continue...", 1, red)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 4 * 3 - text.get_height() // 2))
    pygame.display.update()
    clicked = False
    while not clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True


def main():
    win = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    pygame.display.set_caption("ChessL")
    board = Board(fen="6k1/4nppp/8/8/8/8/5PPP/1Q4K1 w")#6k1/4rppp/8/8/8/8/5PPP/1Q4K1 w
    clock = pygame.time.Clock()
    selected_pos = ()
    marked_pos = [[0] * 8 for _ in range(8)]
    en_passant = ()
    valid_moves = []
    turn = board.turn
    move_text = ""
    last_move = []
    started = False
    black_time = 15 * 60
    white_time = 15 * 60

    selected = False
    start_time = time.time()
    run = True
    while run:
        clock.tick(60)
        if started:
            if turn == WHITE:
                white_time -= time.time() - start_time
            else:
                black_time -= time.time() - start_time

            start_time = time.time()
        else:
            start_time = time.time()
        draw_window(win, board, valid_moves, turn, marked_pos, int(black_time), int(white_time), last_move, move_text)
        board.get_score()
        if board.checkdraw():
            print("Draw!")
            game_over(win, turn, board, tie=True)
            main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.undo_move()
                    turn = change_turn(turn)

                if event.key == pygame.K_RIGHT:
                    board.redo_moves()
                    turn = change_turn(turn)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    m_x, m_y = event.pos
                    if m_x < WIDTH:
                        for i in range(8):
                            for j in range(8):
                                marked_pos[i][j] = 0
                                if board.board[i][j] != 0:
                                    x, y = pygame.mouse.get_pos()
                                    if board.board[i][j].onclick(x, y):
                                        selected = True
                                        board.board[i][j].selected = True
                                        selected_pos = (i, j)
                                        if board.board[selected_pos[0]][selected_pos[1]].color == turn:
                                            if isinstance(board.board[i][j], Pawn):
                                                for move in board.board[i][j].get_valid_moves(board, en_p=en_passant):
                                                    if board.is_legal_move(turn, (selected_pos[0], selected_pos[1]), move):
                                                        valid_moves.append(move)
                                            else:
                                                for move in board.board[i][j].get_valid_moves(board):
                                                    if board.is_legal_move(turn, (selected_pos[0], selected_pos[1]), move):
                                                        valid_moves.append(move)
                                        # print(valid_moves)

                elif pygame.mouse.get_pressed()[2]:
                    for j in range(8):
                        for i in range(8):
                            m_x, m_y = pygame.mouse.get_pos()
                            if onclick(i * W, j * W, m_x, m_y):
                                if marked_pos[i][j] == 1:
                                    marked_pos[i][j] = 0
                                else:
                                    marked_pos[i][j] = 1

            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = event.pos
                selected = False
                x, y = 0, 0
                if m_x < WIDTH:
                    x, y = get_pos(m_x, m_y)
                    if selected_pos:
                        # check who's turn
                        if turn == board.board[selected_pos[0]][selected_pos[1]].color:
                            if (x, y) != selected_pos:
                                if (x, y) in valid_moves:
                                    if board.board[x][y] == 0 or board.board[x][y].color != board.board[selected_pos[0]][selected_pos[1]].color:
                                        if board.board[x][y] == 0:
                                            MOVE.play()
                                        if board.board[x][y] != 0 and board.board[x][y].color != board.board[selected_pos[0]][selected_pos[1]].color:
                                            CAPTURE.play()
                                        prev_board = board.get_board()

                                        move_text = board.move(selected_pos, (x, y))

                                        if not started:
                                            START_END.play()
                                        started = True
                                        last_move = [selected_pos, (x, y)]
                                        if isinstance(board.board[x][y], Rook):
                                            board.board[x][y].castled = True

                                        if isinstance(board.board[x][y], King):
                                            if turn == WHITE:
                                                if not board.board[x][y].s_castled:
                                                    # o-o
                                                    if board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O:
                                                        if board.board[7][7] != 0:
                                                            if not board.board[7][7].castled:
                                                                move_text = board.move((7, 7), (5, 7), castles=O_O)
                                                                board.board[x][y].s_castled = True
                                                                board.board[5][7].castled = True

                                                if not board.board[x][y].l_castled:
                                                    # o-o-o
                                                    if board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O_O:
                                                        if board.board[0][7] != 0:
                                                            if not board.board[0][7].castled:
                                                                move_text = board.move((0, 7), (3, 7), castles=O_O_O)
                                                                board.board[x][y].l_castled = True
                                                                board.board[3][7].castled = True

                                            else:
                                                if not board.board[x][y].s_castled:
                                                    # o-o
                                                    if board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O:
                                                        if board.board[7][0] != 0:
                                                            if not board.board[7][0].castled:
                                                                move_text = board.move((7, 0), (5, 0), castles=O_O)
                                                                board.board[x][y].s_castled = True
                                                                board.board[5][0].castled = True
                                                if not board.board[x][y].s_castled:
                                                    # o-o-o
                                                    if board.board[x][y].is_move_castle(selected_pos[0], selected_pos[1]) == O_O_O:
                                                        if board.board[0][0] != 0:
                                                            if not board.board[0][0].castled:
                                                                move_text = board.move((0, 0), (3, 0), castles=O_O_O)
                                                                board.board[x][y].l_castled = True
                                                                board.board[3][0].castled = True

                                        if isinstance(board.board[x][y], Pawn):
                                            board.board[x][y].first = False
                                            if board.board[x][y].is_move_en_passant(selected_pos, en_passant):
                                                if turn == BLACK:
                                                    board.board[x][y - 1] = 0
                                                else:
                                                    board.board[x][y + 1] = 0
                                                CAPTURE.play()
                                        if abs(y - selected_pos[1]) == 2:
                                            en_passant = (x, y)
                                        else:
                                            en_passant = ()
                                        if board.check(BLACK):
                                            print("black checks!")
                                        if board.check(WHITE):
                                            print("white checks!")
                                        if board.checkmate(BLACK):
                                            print("black checkmate!")
                                            game_over(win, turn, board)
                                            main()
                                        if board.checkmate(WHITE):
                                            print("white checkmate!")
                                            game_over(win, turn, board)
                                            main()
                                        board.played_moves.append(prev_board)
                                        if board.returned_moves:
                                            if board.board != board.returned_moves[-1]:
                                                board.returned_moves = []
                                        turn = change_turn(turn)

                                        print()
                                        board.print_board()
                                        print(move_text)


                                    elif board.board[x][y].color == board.board[selected_pos[0]][selected_pos[1]].color:
                                        board.board[selected_pos[0]][selected_pos[1]].change_pos((selected_pos[0], selected_pos[1]))
                                else:
                                    board.board[selected_pos[0]][selected_pos[1]].change_pos((selected_pos[0], selected_pos[1]))

                        else:
                            board.board[selected_pos[0]][selected_pos[1]].change_pos((selected_pos[0], selected_pos[1]))
                else:
                    board.board[selected_pos[0]][selected_pos[1]].change_pos(selected_pos)
                board.set_every_pos()
                valid_moves = []
                selected_pos = ()
                board.unselectall()

            if event.type == pygame.MOUSEMOTION:
                if selected:
                    x, y = event.pos
                    if x > WIDTH:
                        x = WIDTH
                    img_x = x - W / 2
                    img_y = y - W / 2
                    for j in range(8):
                        for i in range(8):
                            if board.board[i][j] != 0:
                                if board.board[i][j].selected:
                                    board.board[i][j].x = img_x
                                    board.board[i][j].y = img_y

main()

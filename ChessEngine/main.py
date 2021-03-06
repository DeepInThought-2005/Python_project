import pygame
from constants import *
import time
import copy
import random
from board import *
from game import Game

pygame.mixer.init()
pygame.font.init()

a_cool_position = "5B1k/1R6/5p1K/1n1r3p/8/8/8/5b2 w"

# AI part
# def evaluate(max_color):
#     global board
#     if max_color == WHITE:
#         return board.white_score - board.black_score
#     else:
#         return board.black_score - board.white_score
#
#
# def minimax(win, depth, alpha, beta, max_turn, max_color):
#     global board, turn
#     if depth == 0 or board.game_over():
#         return None, evaluate(max_color)
#     moves = []
#     for i in range(8):
#         for j in range(8):
#             if board.board[i][j] != 0:
#                 if board.board[i][j].color == max_turn:
#                     if isinstance(board.board[i][j], Pawn):
#                         for move in board.board[i][j].get_valid_moves(board, en_p=en_passant):
#                             if board.is_legal_move(turn, (i, j), move):
#                                 moves.append([(i, j), move])
#                     else:
#                         for move in board.board[i][j].get_valid_moves(board):
#                             if board.is_legal_move(turn, (i, j), move):
#                                 moves.append([(i, j), move])
#
#     best_move = random.choice(moves)
#
#     if max_turn == WHITE:
#         max_eval = -9999
#         for move in moves:
#             board.move(move[0], move[1])
#             current_eval = minimax(win, depth - 1, alpha, beta, BLACK, max_color)[1]
#             board.redo_moves()
#             board.print_board()
#             if current_eval > max_eval:
#                 best_move = move
#             alpha = max(alpha, current_eval)
#             if beta <= alpha:
#                 break
#         return best_move, max_eval
#
#     else:
#         min_eval = 9999
#         for move in moves:
#             AI_move(win, move[0], move[1])
#             current_eval = minimax(win, depth - 1, alpha, beta, WHITE, max_color)[1]
#             board.redo_moves()
#             board.print_board()
#             if current_eval < min_eval:
#                 min_eval  = current_eval
#                 best_move = move
#             beta = min(beta, current_eval)
#             if beta <= alpha:
#                 break
#         return best_move, min_eval


# def game_over(win, turn, board, tie=False, stalemate=False):
#     START_END.play()
#     turn = change_turn(turn)
#     # win.fill(black)
#     board.set_every_pos()
#     # board.set_every_coord()
#     board.unselectall()
#
#     # draw the board again
#     board.draw(win)
#     for i in range(8):
#         for j in range(8):
#             if board.board[i][j] != 0:
#                 board.board[i][j].draw(win)
#
#     text_font = pygame.font.SysFont("times", 100)
#     hint_font = pygame.font.SysFont("times", 60)
#     if tie:
#         text = text_font.render("Draw!", 1, red)
#     elif stalemate:
#         text = text_font.render(change_turn(turn) + ' stalemates!', 1, red)
#     else:
#         text = text_font.render(turn + ' checkmates!', 1, red)
#     hint = hint_font.render("click anywhere to continue...", 1, red)
#     win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
#     win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 4 * 3 - text.get_height() // 2))
#     pygame.display.update()
#     clicked = False
#     while not clicked:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 quit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 clicked = True


def get_square_onclick(m_x, m_y):
    for j in range(8):
        for i in range(8):
            if m_x >= i * W and m_x <= i * W + W and m_y >= j * W and m_y <= j * W + W:
                return i, j

def main():
    win = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    pygame.display.set_caption("ChessL")
    clock = pygame.time.Clock()
    black_time = 15 * 60
    white_time = 15 * 60
    selected = False
    start_time = time.time()

    game = Game()

    run = True
    while run:
        clock.tick(60)
        if game.gameover:
            main()
        if game.started:
            if game.turn == WHITE:
                white_time -= time.time() - start_time
            else:
                black_time -= time.time() - start_time
            start_time = time.time()
        else:
            start_time = time.time()

        game.draw_window(win, int(black_time), int(white_time))
        game.board.get_score()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.undo_move()

                if event.key == pygame.K_RIGHT:
                    game.redo_move()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = event.pos
                if m_x < WIDTH:
                    x, y = game.get_onclick(m_x, m_y)
                    if pygame.mouse.get_pressed()[0]:
                        game.marked_pos = [[0] * 8 for _ in range(8)]
                        if x != -1:
                            selected = True
                            game.selected_pos = (x, y)
                            game.board.board[x][y].selected = True
                            if game.turn == game.board.board[x][y].color:
                                if isinstance(game.board.board[x][y], Pawn):
                                    valid_moves = game.board.board[x][y].get_valid_moves(game.board, en_p=game.en_passant_pos)
                                else:
                                    valid_moves = game.board.board[x][y].get_valid_moves(game.board)
                                moves = []
                                for move in valid_moves:
                                    if game.board.is_legal_move(game.turn, (x, y), move):
                                        moves.append(move)
                                game.valid_moves = moves

                    x, y = get_square_onclick(m_x, m_y)
                    if pygame.mouse.get_pressed()[2]:
                        if m_x < WIDTH:
                            game.mark((x, y))

            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = event.pos
                selected = False
                if m_x < WIDTH:
                    x, y = get_square_onclick(m_x, m_y)
                    if game.selected_pos:
                        game.make_move(win, game.selected_pos, (x, y))

                game.valid_moves = []
                game.board.set_every_pos()
                game.selected_pos = ()
                game.board.unselectall()

            if event.type == pygame.MOUSEMOTION:
                m_x, m_y = event.pos
                if selected:
                    bo = game.board.board
                    if m_x > WIDTH:
                        m_x = WIDTH
                    img_x = m_x - W / 2
                    img_y = m_y - W / 2
                    for j in range(8):
                        for i in range(8):
                            if bo[i][j] != 0:
                                if bo[i][j].selected:
                                    game.board.board[i][j].x = img_x
                                    game.board.board[i][j].y = img_y

main()

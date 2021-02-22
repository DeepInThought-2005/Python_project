from typing import Tuple
import pygame
pygame.font.init()

WIDTH = 900
HEIGHT = 900
W = WIDTH // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = ""
        self.revealed = False

    def draw(self, win):
        if self.revealed:
            if self.color == 'x':
                font = pygame.font.SysFont("times", 250)
                text = font.render("X", 1, BLACK)
                win.blit(text, (self.x * W + W // 2 - text.get_width() // 2, 
                                self.y * W + W // 2 - text.get_height() // 2))
            else:
                pygame.draw.circle(win, BLACK, (self.x * W + W // 2, self.y * W + W // 2), W // 2 * 3 // 4, 6)

    def onclick(self, m_x, m_y):
        # 283 24 -> 0, 300
        return m_x > self.x * W and m_x < (self.x + 1) * W and m_y > self.y * W and m_y < (self.y + 1) * W

'''
[[x, x, x],
 [o, x, x],
 [o, o, x]]

'''

# check horizontaly
def check_h(row, turn, board):
    for i in range(3):
        if board[i][row].color != turn:
            return False
    return True

# check verticaly
def check_v(col, turn, board):
    for j in range(3):
        if board[col][j].color != turn:
            return False
    return True


# check diagonaly right_down
def check_drd(turn, board):
    '''
        [x,
            x,
                x]
    '''
    for i in range(3):
        for j in range(3):
            if i == j and board[i][j].color != turn:
                return False
    return True

# check diagonaly left_down
def check_dld(turn, board):
    '''
    [       x, 2 | 0
        x,     1 | 1
    x]         0 | 2
    '''

    if board[2][0].color == turn and \
       board[1][1].color == turn and \
       board[0][2].color == turn:
        return True


def check_winner(turn, board):
    for i in range(3):
        if check_h(i, turn, board) or check_v(i, turn, board):
            return True
    if check_dld(turn, board) or check_drd(turn, board):
        return True
    return False

def check_tie(board):
    for i in range(3):
        for j in range(3):
            if not board[i][j].color:
                return False

    return True

def draw_grid(win):
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(win, BLACK, (i * W, j * W, W, W), 6)

def draw_window(win, board):
    win.fill(WHITE)
    draw_grid(win)
    for i in range(3):
        for j in range(3):
            board[i][j].draw(win)
    pygame.display.update()

def game_over(win, turn, tie=False):
    win.fill(WHITE)
    font = pygame.font.SysFont("times", 250)
    text = ""
    if not tie:
        text = font.render(turn + ' wins!', 1, RED)
    else:
        text = font.render("x tie o!", 1, RED)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1500)


def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TIC TAC TOE")
    turn = 'x'
    board = []

    for i in range(3):
        board.append([])
        for j in range(3):
            board[i].append(Shape(j, i))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for i in range(3):
                        for j in range(3):
                            x, y = pygame.mouse.get_pos()
                            if board[i][j].onclick(x, y) and not board[i][j].revealed:
                                board[i][j].revealed = True
                                board[i][j].color = turn
                                if check_winner(turn, board):
                                    draw_window(win, board)
                                    pygame.time.delay(1500)
                                    game_over(win, turn)
                                    main()
                                if check_tie(board):
                                    draw_window(win, board)
                                    pygame.time.delay(1500)
                                    game_over(win, turn, tie=True)

                                if turn  == 'x':
                                    turn = 'o'
                                
                                else:
                                    turn = 'x'
        draw_window(win, board)



    
main()


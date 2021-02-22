import pygame
from pygame import draw
pygame.font.init()

WIDTH = 900
HEIGHT = 900
COLS = 3
W = WIDTH // COLS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None
        self.revealed = False

    def onclick(self, m_x, m_y):
        for i in range(COLS):
            for j in range(COLS):
                if m_x > self.x * W and m_x < (self.x + 1) * W and m_y > self.y * W and m_y < (self.y + 1) * W:
                    return True
        return False
    
    def draw(self, win):
        # 1/8
        if self.revealed:
            if self.color == 'x':
                # pygame.draw.line(win, BLACK, (self.x * W + self.x * W // 8, 
                #                               self.y * W + self.y * W // 8),
                #                              ((self.x + 1) * W - self.x * W // 8,
                #                               (self.y + 1) * W - self.y * W // 8), 6)

                # pygame.draw.line(win, BLACK, ((self.x + 1) * W - self.x * W // 8, 
                #                               (self.y * W + self.y * W // 8)),
                #                              ((self.x * W + self.x * W // 8, 
                #                               (self.y + 1) * W - self.y * W // 8)), 6)
                font = pygame.font.SysFont("times", 250)
                text = font.render("X", 1, BLACK)
                win.blit(text, (self.x * W + W // 2 - text.get_width() // 2,
                                self.y * W + W // 2 - text.get_height() // 2))

            else:
                pygame.draw.circle(win, BLACK, (self.x * W + W // 2, self.y * W + W // 2), W // 2 // 8 * 6, 6)


def draw_grid(win):
    for i in range(COLS):
        for j in range(COLS):
            pygame.draw.rect(win, BLACK, (i * W, j * W, W, W), 6)

def draw_window(win, board):
    win.fill(WHITE)
    draw_grid(win)
    for i in range(COLS):
        for j in range(COLS):
            board[i][j].draw(win)
    pygame.display.update()

# vertical
def check_v(color, col, board):
    for j in range(COLS):
        if board[col][j].color != color:
            return False
    return True

# horizontal
def check_h(color, row, board):
    for i in range(COLS):
        if board[i][row].color != color:
            return False
    return True

# diagonal left_up to right_down
def check_drd(color, board):
    for i in range(COLS):
        for j in range(COLS):
            if i == j and board[i][j].color != color:
                return False
    return True

# diagonal right_up to left_down
def check_dld(color, board):
    if board[2][0].color == color and \
       board[1][1].color == color and \
       board[0][2].color == color:
        return True


def check_win(turn, board):
    for i in range(COLS):
        if check_h(turn, i, board):
            return True
        if check_v(turn, i, board):
            return True
    if check_dld(turn, board) or check_drd(turn, board):
        return True

    return False

def game_over(win, turn):
    win.fill(WHITE)
    font = pygame.font.SysFont("times", 250)
    text = font.render(turn + " wins!", 1, RED)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1500)



def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TIC TAC TOE")
    turn = 'x'
    board = []
    for i in range(COLS):
        board.append([])
        for j in range(COLS):
            board[i].append(Shape(j, i))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for i in range(COLS):
                        for j in range(COLS):
                            x, y = pygame.mouse.get_pos()
                            if board[i][j].onclick(x, y) and not board[i][j].revealed:
                                board[i][j].color = turn
                                board[i][j].revealed = True
                                if check_win(turn, board):
                                    draw_window(win, board)
                                    pygame.time.delay(1500)
                                    game_over(win, turn)
                                    main()
                                if turn == 'x':
                                    turn = 'o'
                                else:
                                    turn = 'x'
        draw_window(win, board)


main()




    
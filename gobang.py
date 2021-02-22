import pygame
from pygame import draw
pygame.font.init()

WIDTH = 900
HEIGHT = 900
COLS = 10
W = WIDTH // COLS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# how many connect to win
standard_win = 5

class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = ""
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
            if self.color == 'black':
                pygame.draw.circle(win, BLACK, (self.x * W + W // 2 + 1, self.y * W + W // 2 + 1), W // 2 // 20 * 19)

            else:
                pygame.draw.circle(win, BLACK, (self.x * W + W // 2 + 1, self.y * W + W // 2 + 1), W // 2 // 20 * 19, 3)


def draw_grid(win):
    for i in range(COLS):
        for j in range(COLS):
            pygame.draw.rect(win, BLACK, (i * W, j * W, W, W), 2)

def draw_window(win, board):
    win.fill(WHITE)
    draw_grid(win)
    for i in range(COLS):
        for j in range(COLS):
            board[i][j].draw(win)
    pygame.display.update()

# vertical
def check_v(color, col, row, board):
    if row + 5 <= COLS:
        for j in range(standard_win):
            if board[col][row + j].color != color:
                return False
        return True

# horizontal
def check_h(color, col, row, board):
    if col + 5 <= COLS:
        for i in range(standard_win):
            if board[col + i][row].color != color:
                return False
        return True

# diagonal left_up to right_down
def check_drd(color, col, row, board):
    if col + 5 <= COLS and row + 5 <= COLS:
        for i in range(standard_win):
            for j in range(standard_win):
                if i == j and board[col + i][row + j].color != color:
                    return False
        return True

# diagonal right_up to left_down
def check_dld(color, col, row, board):
    # flip board horizontaly
    b = [[0] * COLS for _ in range(COLS)]
    for i in range(COLS):
        for j in range(COLS):
            b[i][j] = board[COLS - 1 - j][i]

    if col + 5 < COLS and row + 5 < COLS:
        for i in range(standard_win):
            for j in range(standard_win):
                if i == j and b[col + i][row + j].color != color:
                    return False
        return True




def check_win(turn, board):
    for i in range(COLS):
        for j in range(COLS):
            if check_h(turn, i, j, board):
                return True
            if check_v(turn, i, j, board):
                return True
            if check_dld(turn, i, j, board):
                return True
            if check_drd(turn, i, j, board):
                return True

    return False

def game_over(win, turn):
    win.fill(WHITE)
    font = pygame.font.SysFont("times", 150)
    text = font.render(turn + " wins!", 1, RED)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1500)



def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gobang")
    turn = 'black'
    board = []
    played_moves = []
    returned_moves = []
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if played_moves:
                        i, j, color = played_moves.pop()
                        returned_moves.append((i, j, color))
                        board[i][j].color = ""
                        board[i][j].revealed = False
                        if turn == 'black':
                            turn = 'white'
                        else:
                            turn = 'black'

                if event.key == pygame.K_RIGHT:
                    if returned_moves:
                        i, j, color = returned_moves.pop()
                        played_moves.append((i, j, color))
                        board[i][j].color = color
                        board[i][j].revealed = True
                        if turn == 'black':
                            turn = 'white'
                        else:
                            turn = 'black'


            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for i in range(COLS):
                        for j in range(COLS):
                            x, y = pygame.mouse.get_pos()
                            if board[i][j].onclick(x, y) and not board[i][j].revealed:
                                if returned_moves:
                                    if (i, j, board[i][j].color) != returned_moves[-1]:
                                        for x in range(len(returned_moves)):
                                            returned_moves = []
                                
                                
                                board[i][j].color = turn
                                played_moves.append((i, j, board[i][j].color))
                                board[i][j].revealed = True
                                if check_win(turn, board):
                                    draw_window(win, board)
                                    pygame.time.delay(1500)
                                    game_over(win, turn)
                                    main()
                                if turn == 'black':
                                    turn = 'white'
                                else:
                                    turn = 'black'
        draw_window(win, board)


main()




    
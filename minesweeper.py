import pygame
pygame.font.init()
import random
import time

COLS = 10
ROWS = 10
HEIGHTS = 20
W = 40
TOTAL_BEES = 10


WIDTH = W * COLS
HEIGHT = W * ROWS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)

def game_over(win, grid):
    for i in range(COLS):
        for j in range(ROWS):
            grid[i][j].revealed = True

    font = pygame.font.SysFont("comicsansms", 60)
    text = font.render("Game Over!", 1, BLACK)
    draw_window(win, grid)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             return

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bee = False
        self.revealed = False
        self.neighbor_count = 0
        self.marked = False
        # if not random.randint(0, 2):
        #     self.bee = True

            
    def draw(self, win):
        pygame.draw.rect(win, BLACK, (self.x * W, self.y * W, W, W), 2)
        if self.revealed:
            if self.bee:
                pygame.draw.circle(win, BLACK, (self.x * W + W // 2, self.y * W + W // 2), W // 2 - W // 8)
            else:
                pygame.draw.rect(win, GRAY, (self.x * W + 2, self.y * W + 2, W - 3, W - 3))
                font = pygame.font.SysFont("comicsansms", 30)
                text = font.render(str(self.neighbor_count), True, BLACK)
                if self.neighbor_count:
                    win.blit(text, (self.x * W + W // 2 - text.get_width() // 2, self.y * W + W // 2 - text.get_height() // 2))


    def count_neighbors(self, grid):
        if self.bee:
            self.neighbor_count = -1
            return
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.x + i
                y = self.y + j
                if x > -1 and x < COLS and y > -1 and y < ROWS:
                    neighbor = grid[self.x + i][self.y + j]
                    if neighbor.bee:
                        total += 1
        self.neighbor_count = total
    
    def mark(self, win):
        if self.marked:
            x = self.x + 1
            y = self.y + 1
            pygame.draw.polygon(win, BLACK, [(x * W - W // 4 * 3, y * W - W // 4 - 2), 
                                            (x * W - W // 4 * 3, y * W - W // 4 * 3 - 2), 
                                            (x * W - W // 4, y * W - W // 2 - 2)])
            pygame.draw.line(win, BLACK, (x * W - W // 4 * 3 + 1, y * W - W // 2 - 2), 
                                         (x * W - W // 4 * 3 + 1, y * W - 5), 4)
        else:
            pygame.draw.rect(win, BLACK, (self.x * W, self.y * W, W, W), 2)

    def fill_all_0(self, grid):
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.x + i
                y = self.y + j
                if x > -1 and x < COLS and y > -1 and y < ROWS:
                    neighbor = grid[self.x + i][self.y + j]
                    if not neighbor.bee and not neighbor.revealed:
                        neighbor.reveal(grid)


    def is_clicked(self, x, y):
        col = self.x * W
        row = self.y * W
        return x > col and x < col + W and y > row and y < row + W

    def reveal(self, grid):
        self.revealed = True
        if self.neighbor_count == 0:
            self.fill_all_0(grid)

def draw_window(win, grid):
    win.fill(WHITE)
    for i in range(COLS):
        for j in range(ROWS):
            grid[i][j].draw(win)
            if grid[i][j].marked:
                grid[i][j].mark(win)
            else:
                pass
    

    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    grid = []
    for i in range(COLS):
        grid.append([])
        for j in range(ROWS):
            grid[i].append(Cell(i, j))

    options = []

    for i in range(COLS):
        for j in range(ROWS):
            options.append((i, j))


    for n in range(TOTAL_BEES):
        index = random.randint(0, len(options) - 1)
        choice = options[index]
        i = choice[0]
        j = choice[1]
        del options[index]
        grid[i][j].bee = True


    for i in range(COLS):
        grid.append([])
        for j in range(ROWS):
            grid[i][j].count_neighbors(grid)

    run = True
    while run:
        draw_window(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for i in range(COLS):
                        for j in range(ROWS):
                            x, y = pygame.mouse.get_pos()
                            if grid[i][j].is_clicked(x, y):
                                if not grid[i][j].marked:
                                    grid[i][j].reveal(grid)
                                    if grid[i][j].bee:
                                        game_over(win, grid)
                                        time.sleep(3)
                                        main()

                elif pygame.mouse.get_pressed()[2]:
                    for i in range(COLS):
                        for j in range(ROWS):
                            x, y = pygame.mouse.get_pos()
                            if grid[i][j].is_clicked(x, y):
                                if not grid[i][j].marked and not grid[i][j].revealed:
                                    grid[i][j].marked = True
                                else:
                                    grid[i][j].marked = False

main()
import pygame
import os


# All constants come here!

# SETUP CONSTANTS
WIDTH = 800
HEIGHT = 800
W = 100

# colors
black = (0, 0, 0)
red = (255, 0, 0)
hell_red = (255, 60, 70)
dark_red = (255, 0, 20)
green = (119, 148, 85)
white = (235, 235, 208)
hell_green = (153, 204, 0)
hell_gray = (192, 192, 192)
hell_orange = (255, 204, 0)
dark_orange = (255, 204, 80)
checked = (255, 128, 128)


# GAME CONSTANTS
BLACK = 'black'
WHITE = 'white'
O_O = 'o-o'
O_O_O = 'o-o-o'

# Piece style
GAMEROOM = "GameRoom"
NEON = "Neon"

PIECESTYLE = GAMEROOM

#IMGS
BOARD = os.path.join(PIECESTYLE, "chessboard.png")

BLACK_KING = os.path.join(PIECESTYLE, "black_king.png")
BLACK_QUEEN = os.path.join(PIECESTYLE, "black_queen.png")
BLACK_ROOK = os.path.join(PIECESTYLE, "black_rook.png")
BLACK_KNIGHT = os.path.join(PIECESTYLE, "black_knight.png")
BLACK_BISHOP = os.path.join(PIECESTYLE, "black_bishop.png")
BLACK_PAWN = os.path.join(PIECESTYLE, "black_pawn.png")

WHITE_KING = os.path.join(PIECESTYLE, "white_king.png")
WHITE_QUEEN = os.path.join(PIECESTYLE, "white_queen.png")
WHITE_ROOK = os.path.join(PIECESTYLE, "white_rook.png")
WHITE_KNIGHT = os.path.join(PIECESTYLE, "white_knight.png")
WHITE_BISHOP = os.path.join(PIECESTYLE, "white_bishop.png")
WHITE_PAWN = os.path.join(PIECESTYLE, "white_pawn.png")


# BOARD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("chess_material", "chessboard.png")), (WIDTH, HEIGHT))



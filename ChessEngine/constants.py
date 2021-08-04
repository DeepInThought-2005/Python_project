import pygame
pygame.mixer.init()
import os

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
valid_move_color = (90, 34, 244)
hell_orange = (255, 204, 0)
dark_orange = (255, 204, 80)
checked = (255, 128, 128)
select_color = (0, 255, 255)

# SOUND CONSTANTS
"""
MOVE = pygame.mixer.Sound(os.path.join("Sound", "Move.ogg"))
CAPTURE = pygame.mixer.Sound(os.path.join("Sound", "Capture.ogg"))
START_END = pygame.mixer.Sound(os.path.join("Sound", "start_end.ogg"))
"""

# GAME CONSTANTS
BLACK = 'black'
WHITE = 'white'
O_O = 'o-o'
O_O_O = 'o-o-o'
CHECKMATE = "checkmate"
STALEMATE = "stalemate"
DRAW = "draw"

# Piece style
STAUNTY = "Staunty"
PIXEL = "Pixel"
LICHESSDEFAULT = "Lichessdefault"

PIECESTYLE = PIXEL

# Board style

BLUE = "blue"

BOARDSTYLE = BLUE

#IMGS
FILETYPE = ".png"
BOARD = os.path.join("Boardstyle", BOARDSTYLE + FILETYPE)

BLACK_KING = os.path.join(PIECESTYLE, "bK" + FILETYPE)
BLACK_QUEEN = os.path.join(PIECESTYLE, "bQ" + FILETYPE)
BLACK_ROOK = os.path.join(PIECESTYLE, "bR" + FILETYPE)
BLACK_KNIGHT = os.path.join(PIECESTYLE, "bN" + FILETYPE)
BLACK_BISHOP = os.path.join(PIECESTYLE, "bB" + FILETYPE)
BLACK_PAWN = os.path.join(PIECESTYLE, "bP" + FILETYPE)

WHITE_KING = os.path.join(PIECESTYLE, "wK" + FILETYPE)
WHITE_QUEEN = os.path.join(PIECESTYLE, "wQ" + FILETYPE)
WHITE_ROOK = os.path.join(PIECESTYLE, "wR" + FILETYPE)
WHITE_KNIGHT = os.path.join(PIECESTYLE, "wN" + FILETYPE)
WHITE_BISHOP = os.path.join(PIECESTYLE, "wB" + FILETYPE)
WHITE_PAWN = os.path.join(PIECESTYLE, "wP" + FILETYPE)


# BOARD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("chess_material", "chessboard.png")), (WIDTH, HEIGHT))



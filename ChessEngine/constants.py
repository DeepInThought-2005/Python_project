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
checked = (255, 128, 128)


# GAME CONSTANTS
BLACK = 'black'
WHITE = 'white'
O_O = 'o-o'
O_O_O = 'o-o-o'

#IMGS
BLACK_KING = "chess_material/black_king.png"
BLACK_QUEEN = "chess_material/black_queen.png"
BLACK_ROOK = "chess_material/black_rock.png"
BLACK_KNIGHT = "chess_material/black_knight.png"
BLACK_BISHOP = "chess_material/black_bishop.png"
BLACK_PAWN = "chess_material/black_pawn.png"

WHITE_KING = os.path.join("chess_material", "white_king.png")
WHITE_QUEEN = os.path.join("chess_material", "white_queen.png")
WHITE_ROOK = os.path.join("chess_material", "white_rock.png")
WHITE_KNIGHT = os.path.join("chess_material", "white_knight.png")
WHITE_BISHOP = os.path.join("chess_material", "white_bishop.png")
WHITE_PAWN = os.path.join("chess_material", "white_pawn.png")


# BOARD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("chess_material", "chessboard.png")), (WIDTH, HEIGHT))



import pygame
import os


# All constants come here!

# SETUP CONSTANTS
WIDTH = 800
HEIGHT = 800
W = 100

# GAME CONSTANTS
BLACK = 'b'
WHITE = 'w'
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



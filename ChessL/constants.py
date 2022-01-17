import os

DEF_WIDTH = DEF_HEIGHT = 800

BLACK = 'black'
WHITE = 'white'
O_O = 'o-o'
O_O_O = 'o-o-o'

# GAME CONSTANTS
BLACK = 'black'
WHITE = 'white'
O_O = 'o-o'
O_O_O = 'o-o-o'
CHECKMATE = "checkmate"
STALEMATE = "stalemate"
DRAW = "draw"

# color
red = (255, 0, 0)
hell_red = (255, 60, 70)
valid_move_color = (90, 34, 244)
checked = (255, 128, 128)
select_color = (0, 255, 255)


# boardstyle
BLUE = 'blue'

BOARDSTYLE = BLUE
FILETYPE = '.png'

BOARD = os.path.join("Boardstyle", BOARDSTYLE + FILETYPE)

# pieces

LICHESSDEFAULT = "LichessDefault"
STAUNTY = "Staunty"

PIECESTYLE = "Image/Pieces/" + STAUNTY

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

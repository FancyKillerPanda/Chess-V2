# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (125, 125, 125)
LIGHT_GREY = (200, 200, 200)

BACKGROUND_COLOUR = LIGHT_GREY

# screen attributes
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
TITLE = "Chess"

# board attributes
TILE_KEY_SIZE = 32
TILE_SIZE = int(SCREEN_HEIGHT / 8 - TILE_KEY_SIZE / 8)
RANK_NUMBERS = [8, 7, 6, 5, 4, 3, 2, 1]
FILE_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h"]
TUPLE_POSITION_NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7]

FONT_NAME = "Calibri"  # font

FPS = 60  # frame rate

# piece types
KING = "King"
QUEEN = "Queen"
ROOK = "Rook"
BISHOP = "Bishop"
KNIGHT = "Knight"
PAWN = "Pawn"

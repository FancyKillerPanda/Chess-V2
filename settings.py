# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (125, 125, 125)
LIGHT_GREY = (200, 200, 200)
YELLOW = (255, 255, 0)
SOFT_GREEN = (0, 155, 0)
SOFT_YELLOW = (155, 155, 0)
SOFT_RED = (155, 0, 0)

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
DEAD_PIECE_SIZE = 80

FONT_NAME = "Calibri"  # font

FPS = 60  # frame rate

# piece types
KING = "King"
QUEEN = "Queen"
ROOK = "Rook"
BISHOP = "Bishop"
KNIGHT = "Knight"
PAWN = "Pawn"

# pawn promotion button dimensions
PROMOTE_BUTTON_WIDTH = 250
PROMOTE_BUTTON_HEIGHT = 75

# path to the Stockfish executable
STOCKFISH_EXE_PATH = r"C:\Users\Sahil\Desktop\Personal\Coding\Stockfish\Stockfish 9\Windows\stockfish_9_x64.exe"

# global single- and multi-player variables
SINGLEPLAYER = "Singleplayer"
MULTIPLAYER = "Multiplater"

# start screen button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

# difficulty of Stockfish (represents search depth)
EASY = 1
MEDIUM = 4
HARD = 10

from os import path

import pygame
import pygbutton
from pygame.locals import *
from stockfish import Stockfish

from settings import *
from sprites import *


class Game:
    """Main class that represents the actual game."""

    def __init__(self):
        """Initialises the game window and game elements."""

        #  initialises PyGame's engine
        pygame.init()

        # instance attributes defined outside of __init__
        self.dir = None
        self.image_dir = None

        # creating the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN | HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption(TITLE)

        # variables for running the loops
        self.clock = pygame.time.Clock()
        self.running = True  # game is RUNNING;
        self.playing = False  # not necessarily PLAYING

        # sprite groups
        self.all_sprites_list = pygame.sprite.Group()
        self.tiles_list = pygame.sprite.Group()
        self.pieces_list = pygame.sprite.Group()
        self.dead_pieces_list = pygame.sprite.Group()
        self.highlighted_tiles = pygame.sprite.Group()
        self.buttons_list = pygame.sprite.Group()

        # default font
        self.font_name = pygame.font.match_font(FONT_NAME)

        # piece being highlighted tracker
        self.highlighted_piece = None

        # tracks who's turn it is
        self.turn = WHITE

        # list of moves made
        self.moves_made = []

        # tracks if player is in the process of picking a piece to promote to
        self.promoting = False
        self.pawn_to_promote = None

        # dim rectangle
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha(self.screen)
        self.dim_screen.fill((0, 0, 0, 125))

        # buttons for choice of piece to promote to
        font = pygame.font.Font("freesansbold.ttf", 20)

        self.promote_to_queen = pygbutton.PygButton((SCREEN_WIDTH / 2 - PROMOTE_BUTTON_WIDTH / 2,
                                                     SCREEN_HEIGHT / 2 - PROMOTE_BUTTON_HEIGHT * 2,
                                                     PROMOTE_BUTTON_WIDTH, PROMOTE_BUTTON_HEIGHT), "QUEEN", WHITE,
                                                    BLACK, font=font)
        self.promote_to_knight = pygbutton.PygButton((SCREEN_WIDTH / 2 - PROMOTE_BUTTON_WIDTH / 2,
                                                      SCREEN_HEIGHT / 2 - PROMOTE_BUTTON_HEIGHT, PROMOTE_BUTTON_WIDTH,
                                                      PROMOTE_BUTTON_HEIGHT), "KNIGHT", BLACK, WHITE, font=font)
        self.promote_to_bishop = pygbutton.PygButton((SCREEN_WIDTH / 2 - PROMOTE_BUTTON_WIDTH / 2,
                                                      SCREEN_HEIGHT / 2, PROMOTE_BUTTON_WIDTH, PROMOTE_BUTTON_HEIGHT),
                                                     "BISHOP", WHITE, BLACK, font=font)
        self.promote_to_rook = pygbutton.PygButton((SCREEN_WIDTH / 2 - PROMOTE_BUTTON_WIDTH / 2,
                                                    SCREEN_HEIGHT / 2 + PROMOTE_BUTTON_HEIGHT, PROMOTE_BUTTON_WIDTH,
                                                    PROMOTE_BUTTON_HEIGHT), "ROOK", BLACK, WHITE, font=font)

        self.load_data()  # loads all the other data

    def new(self):
        """Starts a new game."""

        # clears sprite groups
        for sprite in self.all_sprites_list:
            sprite.kill()

        # creates and sets up the board
        self.board = Board(self)
        self.setup_board()

        # initialises the Stockfish engine
        self.stockfish = Stockfish(STOCKFISH_EXE_PATH)

        # calls the main loop
        self.run()

    def run(self):
        """Main game loop for running the game."""
        self.playing = True  # now the game is PLAYING

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """Updates the sprites for the game loop."""
        self.all_sprites_list.update()
        self.stockfish.set_position(self.moves_made)

    def events(self):
        """Handles the game's events."""

        # grabs all the PyGame events
        for event in pygame.event.get():

            # if the red cross (top-right corner) is clicked
            if event.type == QUIT:
                self.playing = False  # ends loop in self.run()
                self.running = False  # ends loop outside class

            elif event.type == KEYUP:

                # allows the game to be quit when <escape> is pressed
                if event.key == K_ESCAPE:
                    self.playing = False
                    self.running = False

            # on mouse click
            if event.type == MOUSEBUTTONDOWN:

                # when not currently in the menu to promote a pawn
                if not self.promoting:

                    for tile in self.tiles_list:

                        # moves the piece when a highlighted square is clicked
                        if is_clicked(tile.rect) and self.highlighted_piece is not None:
                            self.highlighted_piece.make_move(tile)

                    for piece in self.pieces_list:

                        if is_clicked(piece.rect):

                            # when the piece is clicked, highlight its legal moves
                            if piece.colour == self.turn:
                                piece.highlight_legal_moves()
                                self.highlighted_piece = piece

            if self.promoting:

                if "click" in self.promote_to_queen.handleEvent(event):
                    self.promoting = False
                    self.pawn_to_promote.promote_pawn(self.pawn_to_promote.promotion_move, QUEEN)

                elif "click" in self.promote_to_knight.handleEvent(event):
                    self.promoting = False
                    self.pawn_to_promote.promote_pawn(self.pawn_to_promote.promotion_move, KNIGHT)

                elif "click" in self.promote_to_bishop.handleEvent(event):
                    self.promoting = False
                    self.pawn_to_promote.promote_pawn(self.pawn_to_promote.promotion_move, BISHOP)

                elif "click" in self.promote_to_rook.handleEvent(event):
                    self.promoting = False
                    self.pawn_to_promote.promote_pawn(self.pawn_to_promote.promotion_move, ROOK)

    def draw(self):
        """Draws the sprites to the screen."""

        # clears the screen
        self.screen.fill(BACKGROUND_COLOUR)

        # draws the dead pieces
        self.draw_dead_pieces()

        # draws everything in the all_sprites_list group
        self.all_sprites_list.draw(self.screen)

        # draws on the dimness when promoting
        if self.promoting:
            self.screen.blit(self.dim_screen, (0, 0))
            self.promote_to_queen.draw(self.screen)
            self.promote_to_knight.draw(self.screen)
            self.promote_to_bishop.draw(self.screen)
            self.promote_to_rook.draw(self.screen)

        pygame.display.flip()

    def show_start_screen(self):
        """Shows the introductory start screen."""
        pass

    def show_game_over_screen(self):
        """Shows the game over screen."""
        pass

    def draw_text(self, text, size, colour, x, y, surface, bold=False, italics=False):
        """Makes drawing text to the screen easier."""
        font = pygame.font.SysFont(self.font_name, size, bold, italics)  # creates a font
        text_surface = font.render(text, True, colour)  # renders the text
        text_rect = text_surface.get_rect(center=(x, y))  # centers the text

        surface.blit(text_surface, text_rect)  # blits the text to the screen

    def wait_for_key(self):
        """Waits for any key to be pressed by the user."""
        waiting = True

        while waiting:
            self.clock.tick(FPS)

            # grabs events and handles closing of the game and end of waiting
            for event in pygame.event.get():

                if event.type == QUIT:
                    waiting = False
                    self.running = False

                if event.type == KEYUP:
                    waiting = False

    def load_data(self):
        """Loads the external data for the game."""

        # directory that the main.py file is in
        self.dir = path.dirname(__file__)

        # image directory
        self.image_dir = path.join(self.dir, "Images")

    def setup_board(self):
        """Sets up the board to the starting position."""

        # black pawns
        for column in range(8):
            Pawn(self, BLACK, 1, column)

        # white pawns
        for column in range(8):
            Pawn(self, WHITE, 6, column)

        # first row of black pieces
        Rook(self, BLACK, 0, 0)
        Knight(self, BLACK, 0, 1)
        Bishop(self, BLACK, 0, 2)
        Queen(self, BLACK, 0, 3)
        King(self, BLACK, 0, 4)
        Bishop(self, BLACK, 0, 5)
        Knight(self, BLACK, 0, 6)
        Rook(self, BLACK, 0, 7)

        # first row of white pieces
        Rook(self, WHITE, 7, 0)
        Knight(self, WHITE, 7, 1)
        Bishop(self, WHITE, 7, 2)
        Queen(self, WHITE, 7, 3)
        King(self, WHITE, 7, 4)
        Bishop(self, WHITE, 7, 5)
        Knight(self, WHITE, 7, 6)
        Rook(self, WHITE, 7, 7)

    def draw_dead_pieces(self):
        """Draws the dead pieces on the side of the board."""

        white_x = TILE_SIZE * 8 + TILE_KEY_SIZE + 50
        white_y = 50
        black_x = TILE_SIZE * 8 + TILE_KEY_SIZE + 50
        black_y = SCREEN_HEIGHT - 50

        white_piece_count = 0
        black_piece_count = 0

        for piece in self.dead_pieces_list:

            if piece.colour == WHITE:
                white_piece_count += 1
                piece.rect.topleft = white_x, white_y

                white_x += DEAD_PIECE_SIZE + 10

                if white_piece_count == 6:
                    white_piece_count = 0
                    white_y += DEAD_PIECE_SIZE + 10
                    white_x = TILE_SIZE * 8 + TILE_KEY_SIZE + 60

            elif piece.colour == BLACK:
                black_piece_count += 1
                piece.rect.bottomleft = black_x, black_y

                black_x += DEAD_PIECE_SIZE + 10

                if black_piece_count == 6:
                    black_piece_count = 0
                    black_y -= DEAD_PIECE_SIZE + 10
                    black_x = TILE_SIZE * 8 + TILE_KEY_SIZE + 60


if __name__ == "__main__":
    game = Game()
    game.show_start_screen()

    while game.running:
        game.new()

        if game.running:
            game.show_game_over_screen()

    pygame.quit()
    raise SystemExit

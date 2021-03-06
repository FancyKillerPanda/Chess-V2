from re import split
from os.path import join

import pygame
import pygbutton

from settings import *

vector = pygame.math.Vector2


def tuple_to_fen_pos(position):
    """
    Converts a position on the board as a tuple to a FEN string.

    Examples:
        (3, 4) -> 'e5'
        (7, 7) -> 'h1'
        (7, 0) -> 'a1'
    """

    file = position[1]
    rank = position[0]

    if 0 <= file < 8 and 0 <= rank < 8:
        file = chr(97 + file)
        rank = 8 - rank

    else:
        print(f"Invalid board position - File or Rank out of range. {rank}, {file}")

        return

    return file + str(rank)


def fen_pos_to_tuple(position):
    """
    Converts a FEN position on the board to a tuple (starting from the top-left).

    Examples:
        'e5' -> (3, 4)
        'h1' -> (7, 7)
        'a1' -> (7, 0)
    """

    file = position[0]
    rank = int(position[1])

    if file in FILE_LETTERS and rank in RANK_NUMBERS:
        file = ord(file) - 97
        rank = 8 - rank

    else:
        print("Invalid board position - File or Rank out of range.")

        return

    return rank, file


# noinspection PyArgumentList
def tuple_to_pixel_position(position):
    """Converts a tuple position to an (x, y) on the screen."""
    return vector(position[1] * TILE_SIZE + TILE_KEY_SIZE, position[0] * TILE_SIZE)


def is_clicked(rect):
    """Returns True if the piece / tile has been clicked, else False."""
    mouse_pos = pygame.mouse.get_pos()

    if rect.left < mouse_pos[0] < rect.right and rect.top < mouse_pos[1] < rect.bottom:
        return True

    return False


class BreakIter(Exception):
    pass


class Board(pygame.sprite.Sprite):
    """Represents the board and tracks the pieces on it."""

    def __init__(self, game):
        """Constructs the board."""
        self.groups = game.all_sprites_list
        super().__init__(self.groups)
        self.game = game

        self.image = pygame.Surface((TILE_SIZE * 8 + TILE_KEY_SIZE, TILE_SIZE * 8 + TILE_KEY_SIZE))
        self.image.fill(LIGHT_GREY)
        self.rect = self.image.get_rect()

        for rank in TUPLE_POSITION_NUMBERS:

            for file in FILE_LETTERS:
                file_num = ord(file) - 97

                if (rank + file_num) % 2 == 0:
                    Tile(game, file_num, rank, WHITE, self.image)

                else:
                    Tile(game, file_num, rank, GREY, self.image)

        self.show_rank_numbers()
        self.show_file_letters()

    def show_rank_numbers(self):
        """Shows the rank numbers beside the ranks."""

        x = TILE_KEY_SIZE / 2
        y = TILE_SIZE / 2

        for number in RANK_NUMBERS:
            self.game.draw_text(str(number), 26, BLACK, x, y, self.image, True)
            y += TILE_SIZE

    def show_file_letters(self):
        """Shows the file letters below the files."""

        x = TILE_KEY_SIZE + TILE_SIZE / 2
        y = SCREEN_HEIGHT - TILE_KEY_SIZE / 2

        for letter in FILE_LETTERS:
            self.game.draw_text(letter, 26, BLACK, x, y, self.image, True)
            x += TILE_SIZE


class Tile(pygame.sprite.Sprite):
    """Represents an individual tile on the board."""

    def __init__(self, game, file, rank, colour, board_surface):
        """Constructs the tile."""
        self.groups = game.all_sprites_list, game.tiles_list
        super().__init__(self.groups)
        self.game = game

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(colour)
        self.rect = self.image.get_rect(x=file * TILE_SIZE + TILE_KEY_SIZE, y=rank * TILE_SIZE)

        self.tuple_position = (rank, file)
        self.fen_position = tuple_to_fen_pos(self.tuple_position)

        board_surface.blit(self.image, self.rect)

        self.colour = colour

    def highlight(self, colour=RED):
        """Highlights the tile with a semi-transparent red colour."""

        block = pygame.Surface((TILE_SIZE, TILE_SIZE))
        block.set_alpha(155)
        block.fill(colour)

        self.image.blit(block, (0, 0))
        self.game.highlighted_tiles.add(self)

    def remove_highlight(self):
        self.image.fill(self.colour)
        self.game.highlighted_tiles.remove(self)


# noinspection PyArgumentList
class Piece(pygame.sprite.Sprite):
    """Represents the base class for the pieces."""

    def __init__(self, game, image_name, colour, piece_type, row, column):
        self.groups = game.all_sprites_list, game.pieces_list
        super().__init__(self.groups)
        self.game = game

        self.image_pic = pygame.image.load(join(game.image_dir, image_name)).convert_alpha()
        self.image = pygame.transform.scale(self.image_pic, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(x=column * TILE_SIZE + TILE_KEY_SIZE, y=row * TILE_SIZE)

        self.tuple_position = row, column
        self.fen_position = tuple_to_fen_pos((self.tuple_position[0], self.tuple_position[1]))
        self.pixel_position = tuple_to_pixel_position(self.tuple_position)

        self.colour = colour
        self.piece_type = piece_type

        self.promotion_move = None

        self.change_amount = vector(0, 0)

    def highlight_legal_moves(self):
        """Highlights all the legal moves on the board."""

        for tile in self.game.highlighted_tiles:
            tile.remove_highlight()

        for tile in self.game.tiles_list:
            move = "".join([self.fen_position, tile.fen_position])

            if self.game.stockfish.is_move_correct(move):

                if self.piece_type == KING and abs(tile.tuple_position[1] - self.tuple_position[1]) == 2:
                    tile.highlight(BLUE)

                else:
                    tile.highlight()

            elif self.game.stockfish.is_move_correct("".join([move, "Q"])):
                tile.highlight(GREEN)

    def make_move(self, new_location):
        """Makes a move to a new location if it's legal, else returns None."""

        old_tuple_pos = self.tuple_position
        old_fen_pos = self.fen_position
        old_pixel_pos = self.pixel_position
        new_fen_pos = new_location.fen_position
        move = "".join([old_fen_pos, new_fen_pos])

        if self.game.stockfish.is_move_correct(move):
            self.fen_position = new_fen_pos
            self.tuple_position = fen_pos_to_tuple(self.fen_position)
            self.pixel_position = tuple_to_pixel_position(self.tuple_position)

            if self.piece_type == KING and abs(new_location.tuple_position[1] - old_tuple_pos[1]) == 2:
                self.castle(new_location)

            self.animate_move(old_pixel_pos, self.pixel_position)

            self.check_kill_piece()

            for tile in self.game.highlighted_tiles:
                tile.remove_highlight()

            self.game.moves_made.append(move)

            self.game.swap_turns()
            self.game.highlighted_piece = None

        elif self.game.stockfish.is_move_correct("".join([move, "Q"])) and self.game.game_mode == MULTIPLAYER:
            self.fen_position = new_fen_pos
            self.tuple_position = fen_pos_to_tuple(self.fen_position)
            self.pixel_position = tuple_to_pixel_position(self.tuple_position)

            self.animate_move(old_pixel_pos, self.pixel_position)

            self.check_kill_piece()

            for tile in self.game.highlighted_tiles:
                tile.remove_highlight()

            self.game.promoting = True
            self.promotion_move = move
            self.game.pawn_to_promote = self

            self.game.swap_turns()
            self.game.highlighted_piece = None

    def check_kill_piece(self):
        """Checks if a piece should be killed and, if it should, kills it."""

        for piece in self.game.pieces_list:

            if piece.fen_position == self.fen_position and piece != self:
                self.game.pieces_list.remove(piece)
                self.game.dead_pieces_list.add(piece)

                piece.tuple_position = (-1, -1)
                piece.fen_position = "z0"
                piece.image = pygame.transform.scale(piece.image_pic, (DEAD_PIECE_SIZE, DEAD_PIECE_SIZE))

    def castle(self, new_location):
        """Castles the King and Rook."""

        for piece in self.game.pieces_list:

            if new_location.fen_position == "g1":

                if piece.fen_position == "h1":
                    piece.move_in_castle("f1")

            elif new_location.fen_position == "c1":

                if piece.fen_position == "a1":
                    piece.move_in_castle("d1")

            elif new_location.fen_position == "g8":

                if piece.fen_position == "h8":
                    piece.move_in_castle("f8")

            elif new_location.fen_position == "c8":

                if piece.fen_position == "a8":
                    piece.move_in_castle("d8")

    def move_in_castle(self, new_location):
        """Moves the Rook during a castle."""

        old_pixel_pos = self.pixel_position
        self.fen_position = new_location
        self.tuple_position = fen_pos_to_tuple(self.fen_position)
        self.pixel_position = tuple_to_pixel_position(self.tuple_position)

        self.animate_move(old_pixel_pos, self.pixel_position)
        # self.rect = self.image.get_rect(topleft=self.pixel_position)

    def promote_pawn(self, move, chosen_piece):
        """Allows a pawn to be promoted to a different piece."""

        position = self.tuple_position
        self.kill()
        # self.game.promoting = False

        if chosen_piece == QUEEN:
            Queen(self.game, self.colour, position[0], position[1])
            self.game.moves_made.append("".join([move, "Q"]))

        elif chosen_piece == KNIGHT:
            Knight(self.game, self.colour, position[0], position[1])
            self.game.moves_made.append("".join([move, "N"]))

        elif chosen_piece == BISHOP:
            Bishop(self.game, self.colour, position[0], position[1])
            self.game.moves_made.append("".join([move, "B"]))

        elif chosen_piece == ROOK:
            Rook(self.game, self.colour, position[0], position[1])
            self.game.moves_made.append("".join([move, "R"]))

        self.promotion_move = None

    def animate_move(self, old_pos, new_pos):
        self.change_amount = new_pos - old_pos

    def update(self):
        self.rect.x += self.change_amount.x / 46
        self.rect.y += self.change_amount.y / 46

        if self.rect.topleft == tuple(tuple_to_pixel_position(self.tuple_position)):
            self.change_amount = vector(0, 0)


class King(Piece):
    """Class to represent the King piece."""

    def __init__(self, game, colour, row, column):
        """Constructs the King."""

        piece_type = KING

        if colour == WHITE:
            image = "White King.png"

        else:
            image = "Black King.png"

        super().__init__(game, image, colour, piece_type, row, column)


class Queen(Piece):
    """Class to represent the Queen piece."""

    def __init__(self, game, colour, row, column):
        """Constructs the Queen."""

        piece_type = QUEEN

        if colour == WHITE:
            image = "White Queen.png"

        else:
            image = "Black Queen.png"

        super().__init__(game, image, colour, piece_type, row, column)


class Rook(Piece):
    """Class to represent the Rook piece."""

    def __init__(self, game, colour, row, column):
        """Constructs the Rook."""

        piece_type = BISHOP

        if colour == WHITE:
            image = "White Rook.png"

        else:
            image = "Black Rook.png"

        super().__init__(game, image, colour, piece_type, row, column)


class Bishop(Piece):
    """Class to represent the Bishop piece."""

    def __init__(self, game, colour, row, column):
        """Constructs the Bishop."""

        piece_type = BISHOP

        if colour == WHITE:
            image = "White Bishop.png"

        else:
            image = "Black Bishop.png"

        super().__init__(game, image, colour, piece_type, row, column)


class Knight(Piece):
    """Class to represent the Knight piece."""

    def __init__(self, game, colour, row, column):
        """Constructs the Knight."""

        piece_type = KNIGHT

        if colour == WHITE:
            image = "White Knight.png"

        else:
            image = "Black Knight.png"

        super().__init__(game, image, colour, piece_type, row, column)


class Pawn(Piece):
    """Class to represent the Pawn piece."""

    def __init__(self, game, colour, row, column):
        """Constructs the Pawn."""

        piece_type = PAWN

        if colour == WHITE:
            image = "White Pawn.png"

        else:
            image = "Black Pawn.png"

        super().__init__(game, image, colour, piece_type, row, column)

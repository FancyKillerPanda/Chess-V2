from re import split
from os.path import join

import pygame

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

        self.tuple_position = vector(row, column)
        self.fen_position = tuple_to_fen_pos((int(self.tuple_position[0]), int(self.tuple_position[1])))

        self.colour = colour
        self.piece_type = piece_type

    def is_clicked(self):
        """Returns True if the piece has been clicked, else False."""
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            return True

        return False

    def highlight_legal_moves(self):
        """Highlights all the legal moves on the board."""

        for tile in self.game.highlighted_tiles:
            tile.remove_highlight()

        for tile in self.game.tiles_list:
            move = "".join([self.fen_position, tile.fen_position])

            if self.game.stockfish.is_move_correct(move):
                tile.highlight()


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


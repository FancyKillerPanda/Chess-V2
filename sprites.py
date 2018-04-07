import pygame

from settings import *


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


def setup_board(fen_position):
    """Takes a FEN string as a parameter and places pieces on the board accordingly."""


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


class Piece(pygame.sprite.Sprite):
    """Represents the base class for the pieces."""

    def __init__(self, game, image_name):
        self.groups = game.all_sprites_list, game.pieces_list
        super().__init__(self.groups)
        self.game = game

        self.image_pic = pygame.image.load(image_name).convert_alpha()
        self.image = pygame.transform.scale(self.image_pic, (TILE_SIZE, TILE_SIZE))


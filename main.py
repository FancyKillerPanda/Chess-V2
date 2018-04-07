from os import path

import pygame
from pygame.locals import *

from settings import *
from sprites import *


class Game:
    """Main class that represents the actual game."""

    def __init__(self):
        """Initialises the game window and game elements."""
        pygame.init()  # initialises pygame's engine

        # instance attributes defined outside of __init__

        self.dir = None
        self.image_dir = None

        # creating the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
        pygame.display.set_caption(TITLE)

        # variables for running the loops
        self.clock = pygame.time.Clock()
        self.running = True  # game is RUNNING;
        self.playing = False  # not necessarily PLAYING

        # sprite groups
        self.all_sprites_list = pygame.sprite.Group()
        self.tiles_list = pygame.sprite.Group()
        self.pieces_list = pygame.sprite.Group()

        self.font_name = pygame.font.match_font(FONT_NAME)

        self.load_data()  # loads all the other data

    def new(self):
        """Starts a new game."""

        # clears sprite groups
        for sprite in self.all_sprites_list:
            sprite.kill()

        self.board = Board(self)

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

    def events(self):
        """Handles the game's events."""

        for event in pygame.event.get():  # gets events

            if event.type == QUIT:
                self.playing = False  # ends loop in self.run()
                self.running = False  # ends loop outside class

            elif event.type == KEYUP:

                if event.key == K_ESCAPE:
                    self.playing = False
                    self.running = False

    def draw(self):
        """Draws the sprites to the screen."""
        self.screen.fill(BACKGROUND_COLOUR)
        self.all_sprites_list.draw(self.screen)

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

            for event in pygame.event.get():

                if event.type == QUIT:
                    waiting = False
                    self.running = False

                if event.type == KEYUP:
                    waiting = False

    def load_data(self):
        """Loads the external data for the game."""
        self.dir = path.dirname(__file__)
        self.image_dir = path.join(self.dir, "Images")


if __name__ == "__main__":
    game = Game()
    game.show_start_screen()

    while game.running:
        game.new()

        if game.running:
            game.show_game_over_screen()

    pygame.quit()
    raise SystemExit

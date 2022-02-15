import pygame.font
from pygame.sprite import Group

import button
from ship import Ship
from button import Button


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (100, 100, 100)
        self.font = pygame.font.SysFont(None, 48)
        self.go_font = pygame.font.SysFont(None, 96)

        # Prepare initial score images.
        self.prep_images()


    def prep_images(self):
        """Prepare initial score images."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_game_over()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, None)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, None)

        # Center High score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw scores and level to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check if current score is the high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, None)

        # Position the level below the current score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_game_over(self):
        """Tell play when game is over."""
        self.game_over_image = self.go_font.render("GAME OVER", True,
                                                (242, 40, 12), None)
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.centerx = self.screen_rect.centerx
        self.game_over_rect.top = self.high_score_rect.bottom + 100

import pygame
from time import sleep
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()

        # Center the ship at bottom of the screen
        self.center_ship()

        # Movement flag.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Center the ship on the screen."""
        # Center the ship at bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a decimal value for the ship's position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Pause.
        sleep(0.2)

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  # Right
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed  # Left
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed  # Down
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed  # Up

        # Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

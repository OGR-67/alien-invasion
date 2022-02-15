import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):
    """A class to represent a single star in the sky."""

    def __init__(self, ai_game):
        """Initialize the star and set its position randomly."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the star image, resize it randomly and set its rect attribute.
        self.size = randint(10, 20)
        self.image = pygame.image.load("images/star.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

        # Start each new star near at random position of the screen.
        self.rect.x = randint(0, self.screen_rect.right)
        self.rect.y = randint(0, self.screen_rect.bottom)

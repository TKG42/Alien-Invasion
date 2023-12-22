import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    """A class to represent a single power-up item for the player."""

    def __init__(self, ai_game):
        """Initialize the power-up and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the power-up image and set its rect attribute.
        self.image = pygame.image.load('images/powerup_t60x60.png')
        self.rect = self.image.get_rect()

        # Start each new power-up near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the power-up's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if power-up is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
  
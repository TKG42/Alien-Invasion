# Part of Alien Invasion game. The bullet class.

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self, ai_game, powerup_active=False):
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		# Create a bullet rect at (0, 0) and then set correct position. 
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)

		if powerup_active:
			self.color = self.settings.powerup_bullet_color
			self.rect.width = self.settings.powerup_bullet_width
			self.rect.height = self.settings.powerup_bullet_height
			self.speed = self.settings.powerup_bullet_speed
		else:
			self.speed = self.settings.bullet_speed

	def update(self):
		"""Move the bullet up the screen."""
		# Update the decimal position of the bullet.
		self.y -= self.settings.bullet_speed
		# Update the rect position
		self.rect.y = self.y 

	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)

		
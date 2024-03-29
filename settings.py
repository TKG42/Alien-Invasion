# Setting class for Alien Invasion game. 

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230) # Set the background color. (R, G, B). Range is 0 - 255 for each color.

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3 # Original value is '3'. Alter for testing 
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.bullet_speed = 1

        # Alien settings
        self.fleet_drop_speed = 10
        
        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Power up settings
        self.powerup_bullet_width = 10 # wider bullet width
        self.powerup_bullet_height = 40 # longer bullet height
        self.powerup_bullet_color = (255, 0, 0) 
        self.powerup_bullet_speed = 1.5 * self.bullet_speed # faster bullets.
        self.powerup_speed = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 0.5
        self.bullet_speed = 1.0
        self.alien_speed = 0.25

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def initialize_hard_dynamic_settings(self):
        """Initialize settings that change during the game, specific to hard mode."""
        self.ship_speed = 0.75
        self.bullet_speed = 2.0
        self.alien_speed = 0.5
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 75

    def initialize_nightmare_dynamic_settings(self):
        """Initialize settings that change during the game, specific to nightmare mode."""
        self.ship_speed = 2.0
        self.bullet_speed = 3.0
        self.alien_speed = 1
        self.fleet_direction = 1 

        # Scoring
        self.alien_points = 200

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        




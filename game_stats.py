class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0
        self.load_high_score()

    def load_high_score(self):
        """Reads from a file to load the high score."""
        try:
            with open('files/high_score.txt') as file_object:
                self.high_score = int(file_object.read().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = 0 # Set to default if the file doesn't exist or content is invalid.

        # TODO: read the high score file

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
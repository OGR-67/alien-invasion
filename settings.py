class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """iniitialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (15, 33, 47)

        # Ship settings
        # self.ship_speed = 4.0
        self.ship_limit = 3

        # Stars settings
        self.star_number = 40

        # Alien settings
        # self.alien_speed = 1.0
        self.fleet_drop_speed = 15
        self.fleet_direction = 1  # 1 for right; -1 for left

        # Bullet settings
        # self.bullet_speed = 3.5
        self.bullet_width = 5.0
        self.bullet_height = 20
        self.bullet_color = (238, 82, 48)
        self.bullet_allowed = 6

        # Difficulty leveling settings
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 6.0
        self.bullet_speed = 8.0
        self.alien_speed = 2.4

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring.
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

import pygame

class Settings():
    """A class for storing all settings of the Alien Invasion game"""

    def __init__(self):
        """Initializes the game settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        # Assigning a background color
        self.bg_color = (230, 230, 230)
        self.bg = pygame.image.load("images/bg.jpg") 

        # Ship settings
        self.ship_limit = 3

        # Bullet parameters
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 5

        # The pace of acceleration of the game
        self.speedup_scale = 1.2

        # The rate of growth of the cost of aliens
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # Scoring points
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """Initializes settings that change during the game"""

        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.3

        # fleet_direction = 1 indicates movement to the right; and -1 - to the left
        self.fleet_direction = 0.5

    def increase_speed(self):
        """Increases speed settings and cost of aliens"""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)

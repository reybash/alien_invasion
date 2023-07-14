import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class representing a single alien"""

    def __init__(self, ai_settings, screen):
        """Initializes the alien and sets its initial position"""

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Uploading an alien image and assigning the rect attribute
        self.image = pygame.image.load("images/alien.png")
        self.rect = self.image.get_rect()

        # Each new alien appears in the upper left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Мaintaining the exact position of the alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Returns True if the alien is at the edge of the screen"""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Moves the alien to the right or to the left"""

        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Displays the alien in the current position"""

        self.screen.blit(self.image, self.rect)

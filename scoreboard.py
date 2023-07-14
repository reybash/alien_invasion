import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        """Initializes scoring attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for invoice output
        self.text_color = (250, 200, 150)
        self.font = pygame.font.SysFont(None, 48)

        # Preparation of invoice images
        self.prep_images()

    def prep_score(self):
        """Converts the current account to a graphical one"""

        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color)

        # Withdrawal of the invoice in the upper right part of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Converts a record score into a graphic image"""

        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color)

        # The record is aligned in the center of the upper side
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Converts the level into a graphic image"""

        self.level_image = self.font.render(str(self.stats.level),
                                            True, self.text_color)

        # The level is displayed under the current account
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Reports the number of remaining ships"""

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def show_score(self):
        """Displays the invoice on the screen"""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Withdrawal of ships
        self.ships.draw(self.screen)

import pygame
from pygame.sprite import Group

from mixer import Mixer
from settings import Settings
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship

import game_functions as gf


def run_game():
    # Initializes the game and creates a screen object
    pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=1024)
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    mixer = Mixer()

    # Creating a Play button
    play_button = Button(screen, "Play")

    # Creating instances of GameStats and Scoreboard
    stats = GameStats(ai_settings)
    stats.init_high_score()

    sb = Scoreboard(ai_settings, screen, stats)

    # Creating a ship, a group of bullets and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Creating a fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Starting the main game cycle
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets, mixer)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, sb,
                              aliens, bullets, mixer)
            gf.update_aliens(ai_settings, stats, sb,
                             screen, ship, aliens, bullets, mixer)

        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, play_button, mixer)


run_game()

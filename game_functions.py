import sys

import pygame

from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets, mixer):
    """Responds to keystrokes"""

    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_p or event.key == pygame.K_RETURN:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        stats.write_high_score()
        sys.exit()
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets, mixer)


def check_keyup_events(event, ship):
    """Reacts to the release of keys"""

    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """Starts a new game when the Play button is clicked"""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_events(ai_settings, screen, stats, sb, play_button,
                 ship, aliens, bullets, gunshot_s):
    """Handles keystrokes and mouse events"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.write_high_score()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen,
                                 stats, sb, ship, aliens, bullets, gunshot_s)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Reset game settings
    ai_settings.initialize_dynamic_settings()

    # Mouse pointer hides
    pygame.mouse.set_visible(False)

    # Reset game statistics
    stats.reset_stats()
    stats.game_active = True

    # Resetting account and level images
    sb.prep_images()

    # Cleaning lists of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Creating a new fleet and placing the ship in the center
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, mixer):
    """Updates the image on the screen and displays a new screen"""

    # The screen is redrawn every time the cycle passes
    screen.fill(ai_settings.bg_color)

    screen.blit(ai_settings.bg, (0, 0))

    # All bullets are displayed behind the images of the ship and the aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Withdrawal of the account
    sb.show_score()

    start_new_level(aliens, bullets, ai_settings,
                    stats, sb, screen, ship, mixer)

    # The Play button is displayed if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Displaying the last drawn screen
    pygame.display.flip()


def fire_bullet(ai_settings, screen, ship, bullets, mixer):
    """Fires a bullet if the maximum has not yet been reached"""

    # Creating a new bullet and including it in the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        pygame.mixer.Channel(0).play(mixer.gunshot_s)
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, stats, sb, aliens, bullets, mixer):
    """Handling collisions of bullets with aliens"""

    # Removing bullets and aliens involved in collisions
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            mixer.explode_s.play()
            pygame.mixer.Channel(2).play(mixer.score_s)

    sb.prep_score()
    check_high_score(stats, sb)


def start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship, mixer):
    if len(aliens) == 0:
        # If the entire fleet is destroyed the next level begins
        bullets.empty()
        ai_settings.increase_speed()

        # Increasing the level
        stats.level += 1
        sb.prep_level()

        pygame.mixer.Channel(1).play(mixer.level_s)
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings, stats, sb, aliens, bullets, explode_s):
    """Update bullet positions and destroys old bullets"""

    # Updating bullet positions
    bullets.update()

    # Removing bullets that have gone beyond the edge of the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, stats, sb, aliens, bullets, explode_s)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determines the number of rows that fit on the screen"""

    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """Calculates the number of aliens in a row"""

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_width, alien_height):
    """Creates an alien places it in a row"""

    alien = Alien(ai_settings, screen)

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Сreates an alien fleet"""

    # Creating an alien and calculating the number of aliens in a row
    # The interval between adjacent aliens is equal to one width of the alien

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # Creating the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number, alien.rect.width, alien.rect.height)


def change_fleet_direction(ai_settings, aliens):
    """Lowers the entire fleet and changes the direction of the fleet"""

    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Reacts to the alien reaching the edge of the screen"""

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, mixer):
    """Handles the collision of a ship with an alien"""

    if stats.ships_left > 0:
        # Reducing ships_left
        stats.ships_left -= 1

        # Updating game information
        sb.prep_ships()

        # Clearing alien and bullet lists
        aliens.empty()
        bullets.empty()

        # Creating a new fleet and placing the ship in the center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        pygame.mixer.Channel(1).play(mixer.hit_s)

        # Pause
        sleep(0.5)

    else:
        pygame.mixer.Channel(0).play(mixer.lose_s)

        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, mixer):
    """Checks if the aliens have reached the bottom of the screen"""

    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            # The same thing happens when a ship collides
            ship_hit(ai_settings, stats, sb, screen,
                     ship, aliens, bullets, mixer)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, mixer):
    """"Checks if the fleet has reached the edge of the screen and then 
    updates the positions of all aliens in the fleet"""

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Checking for "alien-ship" collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, mixer)

    # Checking for aliens that have reached the bottom of the screen
    check_aliens_bottom(ai_settings, stats, sb, screen,
                        ship, aliens, bullets, mixer)


def check_high_score(stats, sb):
    """Checks if a new record has appeared"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import os.path


def check_keydown_events(event, ai_settings, stats, play_button, sb, ship, screen, aliens, bullets):
    """respond to key presses"""
    if event.key == pygame.K_RIGHT:
        # move ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # move ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        save_high_score(stats)
        sys.exit()
    elif event.key == pygame.K_p:
        if stats.game_active == False:
            check_play_button(ai_settings, stats, play_button, sb, ship, screen, aliens, bullets, mouse_x=0, mouse_y=0)
            start_game(ai_settings, stats, sb, ship, screen, aliens, bullets)


def save_high_score(stats):
    high_score_file = 'high_score_file.txt'
    if os.path.isfile(high_score_file):
        with open(high_score_file, 'w') as fo:
            fo.write(str(stats.high_score))
    else:
        with open(high_score_file, 'x') as fo:
            fo.write(str(stats.high_score))


def check_keyup_events(event, ship):
    """respond to key releases"""
    if event.key == pygame.K_RIGHT:
        # stop moving right
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        # stop moving left
        ship.moving_left = False


def check_events(ai_settings, stats, play_button, sb, ship, screen, aliens, bullets):
    """respond to key & mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, play_button, sb, ship, screen, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if stats.game_active == False:
                check_play_button(ai_settings, stats, play_button, sb, ship, screen, aliens, bullets, mouse_x, mouse_y)
                start_game(ai_settings, stats, sb, ship, screen, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # fire bullet (create and add to group)
    if len(bullets) < ai_settings.max_bullet_count:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button):
    """update images on the screen and flip to the new screen"""
    # redraw screen with settings
    screen.fill(ai_settings.bg_colour)
    # draw bullets in the group
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # draw ship, aliens
    ship.blitme()
    aliens.draw(screen)
    # draw score
    sb.show_score()
    # draw play button if the game is inactive
    if stats.game_active == False:
        play_button.draw_button()
    # push out new screen
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    # delete all the old bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check for collisions with aliens"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_scores(stats, sb)
    # replenish the fleet
    if len(aliens) == 0:
        bullets.empty()
        # level-up!
        stats.level += 1
        sb.prep_level()
        ai_settings.increase_speed()
        call_alien_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def call_alien_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = int(get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height))

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """how many rows are required?"""
    available_space_y = (ai_settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = available_space_y / (2 * alien_height)
    return number_rows


def update_aliens(ai_settings, stats, screen, sb, ship, bullets, aliens):
    """update the alien positions"""
    # check for hitting the edge and steer the fleet
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, bullets, aliens)
    # look for aliens hitting the bottom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, sb, ship, bullets, aliens):
        stats.ships_left -= 1
        sb.prep_ships()
        if stats.ships_left > 0:
            pygame.mouse.set_visible(False)
            # clear bullets & aliens
            bullets.empty()
            aliens.empty()
            # recreate fleet & ship
            call_alien_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()
            # pause
            sleep(1)
        else:
            print("Game Over!!")
            stats.game_active = False
            pygame.mouse.set_visible(True)


def check_fleet_edges(ai_settings, aliens):
    """respond when the aliens reach the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """drop the entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """check if aliens get to the bottom of the screen and lose a life"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # same as ship hit
            ship_hit(ai_settings, stats, screen, sb, ship, bullets, aliens)


def check_play_button(ai_settings, stats, play_button, sb, ship, screen, aliens, bullets, mouse_x='', mouse_y=''):
    # deactivate mouse
    pygame.mouse.set_visible(False)
    # start when the button is clicked
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, stats, sb, ship, screen, aliens, bullets)


def start_game(ai_settings, stats, sb, ship, screen, aliens, bullets):
    # reset stats
    stats.reset_stats()
    stats.game_active = True
    pygame.mouse.set_visible(False)
    # redraw scores
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # empty groups
    bullets.empty()
    aliens.empty()
    # new fleet & center ship
    call_alien_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_high_scores(stats, sb):
    """check for new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


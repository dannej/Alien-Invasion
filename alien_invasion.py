import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """Initialize the game"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # make play button
    play_button = Button(ai_settings, screen, "Play")

    # make a ship
    ship = Ship(ai_settings, screen)
    # make a group for bullets to go into
    bullets = Group()
    # make a group of aliens for the fleet
    aliens = Group()

    # call the alien fleet
    gf.call_alien_fleet(ai_settings, screen, ship, aliens)

    # get the stats going
    stats = GameStats(ai_settings)

    # store stats & show scoreboard
    sb = Scoreboard(ai_settings, screen, stats)

    # start main loop
    while True:

        # watch for input
        gf.check_events(ai_settings, stats, play_button, sb, ship, screen, aliens, bullets)

        if stats.game_active:
            # move the ship
            ship.update()
            # move/update bullets on the screen
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # update the alien fleet
            gf.update_aliens(ai_settings, stats, screen, sb,  ship, bullets, aliens)

        # refresh screen
        gf.update_screen(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button)


run_game()

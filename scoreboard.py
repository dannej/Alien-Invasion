import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """report on the scores through the game"""

    def __init__(self, ai_settings, screen, stats):
        """initialise scorekeeping"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # set fonts up
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 32)

        # prepare initial scores
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """make rendered image"""
        self.rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(self.rounded_score)
        self.score_image = self.font.render(str("Score: " + score_str), True, self.text_colour, self.ai_settings.bg_colour)

        # display at top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """draw the scores"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """draw the high score"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(str("High-score: " + high_score_str), True, self.text_colour, self.ai_settings.bg_colour)

        # center at top
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 10

    def prep_level(self):
        """draw the level under the score"""
        self.level_image = self.font.render(str("Level: " + str(self.stats.level)), True, self.text_colour, self.ai_settings.bg_colour)

        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.screen_rect.right - 20
        self.level_image_rect.top = 60

    def prep_ships(self):
        """show remaining ships"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

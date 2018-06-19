import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """a class to represent the alien fleet"""

    def __init__(self, ai_settings, screen):
        """initialise the alien"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load image and set position
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # start the alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store position
        self.x = float(self.rect.x)

    def check_edges(self):
        """return TRUE if we've hit the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """move the fleet along and down towards the ship"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """draw the alien at current location"""
        self.screen.blit(self.image, self.rect)

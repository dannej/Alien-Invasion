import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """make object at current ship position"""
        super().__init__()
        self.screen = screen

        # create a bullet at rect 0,0 and then set new position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store position as float
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """move the bullet up the screen"""
        # update decimal position of the bullet
        self.y -= self.speed_factor
        # now update actual rect position (int only)
        self.rect.y = self.y

    def draw_bullet(self):
        """draw it to screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


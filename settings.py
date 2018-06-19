
class Settings:
    """store all the settings for the game"""

    def __init__(self):
        """initialize"""
        # screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_colour = (230, 230, 230)

        # ship settings
        # self.ship_speed_factor = 2
        self.ship_limit = 3

        # bullet settings
        # self.bullet_speed_factor = 5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.max_bullet_count = 10

        # alien settings
        # self.alien_speed_factor = 2
        self.fleet_drop_speed = 10
        # fleet direction +1 = right, -1 = left
        self.fleet_direction = 1

        # speeding the game up
        self.speedup_scale = 1.2
        self.speedup_score_factor = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """stuff that changes during the game"""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 3
        self.fleet_direction = 1
        # scoring
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.speedup_score_factor * self.alien_points)



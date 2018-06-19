import os.path

class GameStats():
    """track the stats"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.ships_left = self.ai_settings.ship_limit
        self.reset_stats()
        self.game_active = False

        self.high_score = 0
        self.get_high_score_file()

    def reset_stats(self):
        """variable stats that change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score_file(self):
        high_score_file = 'high_score_file.txt'
        if os.path.isfile(high_score_file):
            with open(high_score_file) as fo:
                self.high_score = fo.readline()
                if self.high_score == '':
                    self.high_score = 0
                else:
                    self.high_score = int(self.high_score)
        else:
            self.high_score = 0


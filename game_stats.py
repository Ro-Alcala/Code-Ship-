class GameStats:
    def __init__(self, ai_settings):
        self.ship_limit = ai_settings.ship_limit
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.ship_limit
        self.level = 1
        self.score = 0
        self.game_active = True

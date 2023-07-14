class GameStats():
    """Tracking statistics for the Alien Invasion game"""

    def __init__(self, ai_settings):
        """Initializes statistics"""

        self.ai_settings = ai_settings
        self.reset_stats()

        self.high_score_filename = "high_score.txt"

        # Game starts in idle state
        self.game_active = False

    def reset_stats(self):
        """Initializes statistics that change during the game"""

        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def init_high_score(self):
        read_file = False

        while not read_file:
            try:
                with open(self.high_score_filename) as f_obj:
                    contents = f_obj.read()

                    read_file = True
            except FileNotFoundError:
                with open(self.high_score_filename, 'w') as f_obj:
                    f_obj.write('0')

        try:
            self.high_score = int(contents)
        except ValueError:
            self.high_score = 0

    def write_high_score(self):
        with open(self.high_score_filename, 'w') as f_obj:
            f_obj.write(str(self.high_score))

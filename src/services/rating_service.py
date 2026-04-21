class InvalidPlayerCountError(Exception):
    pass

class RatingService:
    def __init__(self, k_factor=40):
        self._k_factor = k_factor

    def calculate_team_average_rating(self, players):
        if not players:
            raise InvalidPlayerCountError("Team must have at least one player")
        return sum(player.rating for player in players) / len(players)

    def calculate_expected_winratio(self, own_rating, opponent_rating):
        expected_winratio = 1 / (1 + 10 ** ((opponent_rating - own_rating) / 400))
        return expected_winratio

    def calculate_new_rating(self, old_rating, score, expected_winratio):
        new_rating = old_rating + self._k_factor * (score - expected_winratio)
        return round(new_rating)

rating_service = RatingService()

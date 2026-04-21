import random
from entities.player import Player
from repositories.player_repository import (
    player_repository as default_player_repository)
from repositories.match_repository import (
    match_repository as default_match_repository
)
from services.rating_service import rating_service
from entities.match import Match

class PlayerExistsError(Exception):
    pass


class InvalidPlayerNameError(Exception):
    pass


class InvalidTeamSizeError(Exception):
    pass

class SamePlayerError(Exception):
    pass


class GameService:
    def __init__(self, player_repository=default_player_repository, match_repository=default_match_repository):
        self._player_repository = player_repository
        self._match_repository = match_repository

    def create_player(self, name):
        if name == "":
            raise InvalidPlayerNameError("Player name cannot be empty")

        if self._player_repository.get_player_by_name(name) is not None:
            raise PlayerExistsError(
                f"Player with name '{name}' already exists")

        player = Player(name, 1500)
        return self._player_repository.create(player)

    def get_all_players(self):
        return self._player_repository.get_all_players()

    def create_random_teams(self, players: list, team_size):
        if team_size <= 0 or len(players) == 0 or len(players) % team_size != 0:
            raise InvalidTeamSizeError(
                "Player count must be divisible by team size and team size must be greater than 0")

        randomized_players = list(players)
        random.shuffle(randomized_players)
        random_teams = []

        for i in range(0, len(randomized_players), team_size):
            random_teams.append(randomized_players[i:i + team_size])
        return random_teams

    def teams_have_same_player(self, team_a_players, team_b_players):
        team_a_names = {player.name for player in team_a_players}
        team_b_names = {player.name for player in team_b_players}

        for name in team_a_names:
            if name in team_b_names:
                return True
        return False

    def update_player_ratings(self, team_a_players, team_b_players, team_a_won: bool):
        if self.teams_have_same_player(team_a_players, team_b_players):
            raise SamePlayerError("Teams cannot have the same player")

        team_a_average_rating = rating_service.calculate_team_average_rating(
            team_a_players)
        team_b_average_rating = rating_service.calculate_team_average_rating(
            team_b_players)

        team_a_expected_winratio = rating_service.calculate_expected_winratio(
            team_a_average_rating, team_b_average_rating)
        team_b_expected_winratio = rating_service.calculate_expected_winratio(
            team_b_average_rating, team_a_average_rating)

        team_a_score = 1 if team_a_won else 0
        team_b_score = 0 if team_a_won else 1

        for player in team_a_players:
            new_rating = rating_service.calculate_new_rating(
                player.rating, team_a_score, team_a_expected_winratio)
            self._player_repository.update_player_rating(player, new_rating)

        for player in team_b_players:
            new_rating = rating_service.calculate_new_rating(
                player.rating, team_b_score, team_b_expected_winratio)
            self._player_repository.update_player_rating(player, new_rating)

    def save_match_result(self, team_a_players, team_b_players, team_a_points, team_b_points):
        if self.teams_have_same_player(team_a_players, team_b_players):
            raise SamePlayerError("Teams cannot have the same player")
        team_a_player_names = [player.name for player in team_a_players]
        team_b_player_names = [player.name for player in team_b_players]
        match = Match(team_a_player_names, team_b_player_names, team_a_points, team_b_points)

        return self._match_repository.create(match)

game_service = GameService()

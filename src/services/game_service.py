import random
from entities.player import Player
from repositories.player_repository import (
    player_repository as default_player_repository)


class PlayerExistsError(Exception):
    pass


class InvalidPlayerNameError(Exception):
    pass


class InvalidTeamSizeError(Exception):
    pass


class GameService:
    def __init__(self, player_repository=default_player_repository):
        self._player_repository = player_repository

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

game_service = GameService()

from entities.player import Player
from repositories.player_repository import (player_repository as default_player_repository)

class PlayerExistsError(Exception):
    pass

class InvalidPlayerNameError(Exception):
    pass

class GameService:
    def __init__(self, player_repository=default_player_repository):
        self._player_repository = player_repository

    def create_player(self, name):
        if name == "":
            raise InvalidPlayerNameError("Player name cannot be empty")
        
        if self._player_repository.get_player_by_name(name) is not None:
            raise PlayerExistsError(f"Player with name '{name}' already exists")

        player = Player(name, 1500)
        return self._player_repository.create(player)

    def get_all_players(self):
        return self._player_repository.get_all_players()
    
game_service = GameService()
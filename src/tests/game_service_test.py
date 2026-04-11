import unittest
from repositories.player_repository import player_repository
from services.game_service import GameService, PlayerExistsError, InvalidPlayerNameError, InvalidTeamSizeError #pylint:disable=unused-import


class TestGameService(unittest.TestCase):
    def setUp(self):
        player_repository.delete_all()
        self.game_service = GameService()

    def test_create_player_name(self):
        player = self.game_service.create_player("Zonettaja")
        self.assertEqual(player.name, "Zonettaja")

    def test_create_player_rating(self):
        player = self.game_service.create_player("Zonettaja")
        self.assertEqual(player.rating, 1500)
    
    def test_create_randomteams_count(self):
        players = [self.game_service.create_player(str(i)) for i in range(9)]
        teams = self.game_service.create_random_teams(players, 3)
        self.assertEqual(len(teams), 3)
    
    def test_create_random_teams_player_count(self):
        players = [self.game_service.create_player(str(i)) for i in range(9)]
        teams = self.game_service.create_random_teams(players, 3)
        self.assertEqual(len(teams[0]), 3)
    
    def test_create_random_teams_with_invalid_team_size(self):
        players = [self.game_service.create_player(str(i)) for i in range(9)]
        with self.assertRaises(InvalidTeamSizeError):
            self.game_service.create_random_teams(players, 0)

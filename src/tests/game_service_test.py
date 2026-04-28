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

    def test_create_player_with_empty_name(self):
        with self.assertRaises(InvalidPlayerNameError):
            self.game_service.create_player("")

    def test_create_player_with_existing_name(self):
        self.game_service.create_player("Zonettaja")
        with self.assertRaises(PlayerExistsError):
            self.game_service.create_player("Zonettaja")

    def test_get_all_players(self):
        self.game_service.create_player("Zonettaja1")
        self.game_service.create_player("Zonettaja2")
        players = self.game_service.get_all_players()
        self.assertEqual(len(players), 2)

    def test_teams_have_same_player(self):
        player1 = self.game_service.create_player("Zonettaja1")
        team_a = [player1]
        team_b = [player1]
        self.assertTrue(self.game_service.teams_have_same_player(team_a, team_b))
    
    def test_teams_have_different_players(self):
        player1 = self.game_service.create_player("Zonettaja1")
        player2 = self.game_service.create_player("Zonettaja2")
        team_a = [player1]
        team_b = [player2]
        self.assertFalse(self.game_service.teams_have_same_player(team_a, team_b))
    
    def test_update_player_ratings(self):
        player1 = self.game_service.create_player("Zonettaja1")
        player2 = self.game_service.create_player("Zonettaja2")
        team_a = [player1]
        team_b = [player2]
        self.game_service.update_player_ratings(team_a, team_b, team_a_won=True)
        self.assertGreater(player1.rating, 1500)
        self.assertLess(player2.rating, 1500)

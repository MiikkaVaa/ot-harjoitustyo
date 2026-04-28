import unittest
from entities.match import Match
from repositories.match_repository import match_repository

class TestMatchRepository(unittest.TestCase):
    def setUp(self):
        self.match_repository = match_repository
        self.match_repository.delete_all()
        self.team_a_players = ["Aapeli", "Pekka", "Tomi"]
        self.team_b_players = ["Jussi", "Matti", "Aapo"]

    def test_create_match(self):
        game = Match(self.team_a_players, self.team_b_players, 100, 10)
        match_id = self.match_repository.create(game)
        self.assertEqual(match_id, 1)

    def test_get_all_matches(self):
        game1 = Match(self.team_a_players, self.team_b_players, 100, 10)
        game2 = Match(self.team_a_players, self.team_b_players, 150, 20)
        self.match_repository.create(game1)
        self.match_repository.create(game2)
        matches = self.match_repository.get_all_matches()
        self.assertEqual(len(matches), 2)


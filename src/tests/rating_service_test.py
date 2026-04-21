import unittest
from entities.player import Player
from repositories.player_repository import player_repository
from services.rating_service import rating_service, InvalidPlayerCountError

class TestRatingService(unittest.TestCase):
    def setUp(self):
        player_repository.delete_all()
        self.Pelaaja1 = player_repository.create(Player("Pelaaja1", 1500))
        self.Pelaaja2 = player_repository.create(Player("Pelaaja2", 1600))
        self.Pelaaja3 = player_repository.create(Player("Pelaaja3", 1700))
        self.Pelaaja4 = player_repository.create(Player("Pelaaja4", 1500))
        self.Pelaaja5 = player_repository.create(Player("Pelaaja5", 1500))
        self.Pelaaja6 = player_repository.create(Player("Pelaaja6", 1500))

    def test_calculate_team_average_rating(self):
        team1 = [self.Pelaaja1, self.Pelaaja2, self.Pelaaja3]
        team_avg_rating = rating_service.calculate_team_average_rating(team1)
        self.assertEqual(team_avg_rating, 1600)

    def test_calculat_team_average_rating_empty_team(self):
        team1 = []
        with self.assertRaises(InvalidPlayerCountError):
            rating_service.calculate_team_average_rating(team1)

    def test_calculate_expected_winratio(self):
        team1_rating = rating_service.calculate_team_average_rating(
            [self.Pelaaja1, self.Pelaaja2, self.Pelaaja3])
        team2_rating = rating_service.calculate_team_average_rating(
            [self.Pelaaja4, self.Pelaaja5, self.Pelaaja6])

        team1_expected_winratio = rating_service.calculate_expected_winratio(
            team1_rating, team2_rating
            )
        self.assertEqual(round(team1_expected_winratio, 2), 0.64)

    def test_calculate_new_rating(self):
        player_rating = 1500
        score = 1
        expected_winratio = 0.64

        new_rating = rating_service.calculate_new_rating(player_rating, score, expected_winratio)
        self.assertEqual(new_rating, 1514)

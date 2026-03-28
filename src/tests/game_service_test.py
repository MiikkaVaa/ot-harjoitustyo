import unittest
from services.game_service import GameService, PlayerExistsError, InvalidPlayerNameError

class TestGameService(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()
    
    def test_create_player_name(self):
        player = self.game_service.create_player("Zonettaja")
        self.assertEqual(player.name, "Zonettaja")
        
    def test_create_player_rating(self):
        player = self.game_service.create_player("Zonettaja")
        self.assertEqual(player.rating, 1500)


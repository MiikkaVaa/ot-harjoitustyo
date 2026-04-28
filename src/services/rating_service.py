class InvalidPlayerCountError(Exception):
    pass

class RatingService:
    """Rating-arvojen laskemislogiikasta vastaava luokka"
    """

    def __init__(self, k_factor=40):
        """Luokan konstruktori

        Args:
            k_factor: Lukuarvo, joka määrittää rating-arvojen muutoksen suuruuden
        """

        self._k_factor = k_factor

    def calculate_team_average_rating(self, players):
        """Laskee joukkueen rating keskiarvon.

        Args:
            players: Lista Player-oliota, joiden rating-arvoista keskiarvo lasketaan

        Raises:
            InvalidPlayerCountError: Jos joukkueessa ei ole pelaajia

        Returns:
            Joukkueen rating keskiarvo
        """

        if not players:
            raise InvalidPlayerCountError("Team must have at least one player")
        return sum(player.rating for player in players) / len(players)

    def calculate_expected_winratio(self, own_rating, opponent_rating):
        """Laskee joukkueen odotetun voittosuhteen.

        Args:
            own_rating: Lukuarvo, joka kertoo omien pelaajien rating-arvon
            opponent_rating: Lukuarvo, joka kertoo vastustajan pelaajien rating-arvon

        Returns:
            Joukkueen odotettu voittosuhde
        """

        expected_winratio = 1 / (1 + 10 ** ((opponent_rating - own_rating) / 400))
        return expected_winratio

    def calculate_new_rating(self, old_rating, score, expected_winratio):
        """Laskee pelaajan uuden rating-arvon.

        Args:
            old_rating: Lukuarvo, joka kertoo pelaajan vanhan rating-arvon
            score: Lukuarvo, joka kertoo joukkueen pelin lopputuloksen (1 = voitto, 0 = tappio)
            expected_winratio: Lukuarvo, joka kertoo joukkueen odotetun voittosuhteen (0-1)

        Returns:
            Pelaajan uusi rating-arvo pyöristettynä
        """

        new_rating = old_rating + self._k_factor * (score - expected_winratio)
        return round(new_rating)

rating_service = RatingService()

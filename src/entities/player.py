class Player:
    """Luokka, joka määrittelee pelaajan.

    Attributes:
        player_name: Merkkijono, joka kertoo pelaajan nimen
        player_rating: Lukuarvo, joka kertoo pelaajan ratingin

    """
    def __init__(self, player_name, player_rating):
        """Luokan konstruktori, joka luo uuden pelaajan.

        Args:
            player_name: Merkkijono, joka kertoo pelaajan nimen
            player_rating: Lukuarvo, joka kertoo pelaajan ratingin
        """
        self.name = player_name
        self.rating = player_rating

    def update_rating(self, new_rating):
        """Asettaa uuden ratingin pelaajalle

        Args:
            new_rating: Lukuarvo, joka kertoo pelaajan uuden ratingin
        """
        self.rating = new_rating

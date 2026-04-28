from entities.player import Player
from database_connection import get_database_connection


def get_player_by_row(row):
    """Luo pelaaja-olion tietokantarivistä.

    Args:
        row: Tietokantarivi

    Returns:
        _type_:Pelaaja-olio
    """

    return Player(row["name"], row["rating"])

class PlayerRepository:
    """Pelaajiin liittyvistä tietokantaoperaatioista vastaava luokka.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection: Yhteys tietokantaan
        """

        self._connection = connection

    def create(self, player):
        """Tallentaa pelaajan tietokantaa.

        Args:
            player: Player-olio, joka tallennetaan

        Returns:
            Pelaaja-oliom, joka tallennettiin
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO players (name, rating) VALUES (?, ?)", (
                player.name, player.rating)
        )

        self._connection.commit()
        return player

    def get_all_players(self):
        """Hakee kaikki pelaajat tietokannasta.

        Returns:
            list: Lista Player-olioista
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM players")
        rows = cursor.fetchall()
        return [get_player_by_row(row) for row in rows]

    def get_player_by_name(self, name):
        """Hae pelaaja tietokannasta nimen perusteella.

        Args:
            name: Merkkijono pelaajan nimestä

        Returns:
            Player-olio, joka vastaa annettua nimeä, tai None jos pelaajaa ei löydy
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT name, rating FROM players WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return get_player_by_row(row)
        return None

    def update_player_rating(self, player, new_rating):
        """Päivitä pelaajan rating tietokantaan.

        Args:
            player: Player-olio, jonka rating päivitetään
            new_rating: Lukuarvo, joka kertoo pelaajan uuden ratingin
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE players SET rating = ? WHERE name = ?", (new_rating, player.name)
        )
        self._connection.commit()

    def delete_all(self):
        """Poista kaikki pelaajat tietokannasta.
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM players")
        self._connection.commit()


player_repository = PlayerRepository(get_database_connection())

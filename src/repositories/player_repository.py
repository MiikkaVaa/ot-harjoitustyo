from entities.player import Player
from database_connection import get_database_connection


def get_player_by_row(row):
    return Player(row["name"], row["rating"])


class PlayerRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, player):
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO players (name, rating) VALUES (?, ?)", (
                player.name, player.rating)
        )

        self._connection.commit()
        return player

    def get_all_players(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM players")
        rows = cursor.fetchall()
        return [get_player_by_row(row) for row in rows]

    def get_player_by_name(self, name):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT name, rating FROM players WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return get_player_by_row(row)
        return None
    
    def update_player_rating(self, player, new_rating):
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE players SET rating = ? WHERE name = ?", (new_rating, player.name)
        )
        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM players")
        self._connection.commit()


player_repository = PlayerRepository(get_database_connection())

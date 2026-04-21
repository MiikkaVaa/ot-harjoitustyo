from database_connection import get_database_connection
from entities.match import Match

class MatchRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, match):
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO matches (team_a_points, team_b_points) VALUES (?, ?)", (
                match.team_a_points, match.team_b_points)
        )

        match_id = cursor.lastrowid

        for player_name in match.team_a_players:
            cursor.execute(
                "INSERT INTO match_players (match_id, player_name, team_side) VALUES (?, ?, 'A')", (
                    match_id, player_name)
            )

        for player_name in match.team_b_players:
            cursor.execute(
                "INSERT INTO match_players (match_id, player_name, team_side) VALUES (?, ?, 'B')", (
                    match_id, player_name)
            )

        self._connection.commit()
        return match_id

    def get_all_matches(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM matches")
        rows = cursor.fetchall()

        matches = []
        for row in rows:
            cursor.execute(
                "SELECT player_name, team_side FROM match_players WHERE match_id = ?", (row["id"],)
            )
            player_rows = cursor.fetchall()
            team_a_players = []
            team_b_players = []
            for player_row in player_rows:
                if player_row["team_side"] == "A":
                    team_a_players.append(player_row["player_name"])
                else:
                    team_b_players.append(player_row["player_name"])
            matches.append(Match(
                team_a_players, team_b_players, row["team_a_points"], row["team_b_points"]
                ))

        return matches

match_repository = MatchRepository(get_database_connection())

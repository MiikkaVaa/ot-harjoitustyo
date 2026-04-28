import random
from entities.player import Player
from entities.match import Match
from repositories.player_repository import (
    player_repository as df_player_repository)
from repositories.match_repository import (
    match_repository as df_match_repository
)
from services.rating_service import rating_service

class PlayerExistsError(Exception):
    pass

class InvalidPlayerNameError(Exception):
    pass

class InvalidTeamSizeError(Exception):
    pass

class SamePlayerError(Exception):
    pass

class GameService:
    """Sovelluslogiikasta vastaava luokka"
    """

    def __init__(
            self, player_repository=df_player_repository, match_repository=df_match_repository):
        """Luokan konstruktori.

        Args:
            player_repository: 
                Oletuksena PlayerRepository-olio, 
                joka vastaa pelaajiin liittyvistä tietokantaoperaatioista
            match_repository: 
                Oletuksena MatchRepository-olio, 
                joka vastaa peleihin liittyvistä tietokantaoperaatioista
        """

        self._player_repository = player_repository
        self._match_repository = match_repository


    def create_player(self, name):
        """Luo uuden pelaajan.

        Args:
            name: Merkkijono joka kertoo luotavan pelaajan nimen

        Returns:
            Luotu Player-olio
        """

        if name == "":
            raise InvalidPlayerNameError("Player name cannot be empty")

        if self._player_repository.get_player_by_name(name) is not None:
            raise PlayerExistsError(
                f"Player with name '{name}' already exists")

        player = Player(name, 1500)
        return self._player_repository.create(player)

    def get_all_players(self):
        """Hakee kaikki pelaajat tietokannasta.

        Returns:
            Lista Player-olioista, jotka on haettu tietokannasta
        """
        return self._player_repository.get_all_players()

    def create_random_teams(self, players: list, team_size):
        """Luo annetun koon kokoisia satunnaisia joukkueita annetuista pelaajista.

        Args:
            players: Lista Player-olioita
            team_size: Lukuarvo, joka kertoo joukkueen koon

        Returns:
            Lista joukkueita.
        """

        if team_size <= 0 or len(players) == 0 or len(players) % team_size != 0:
            raise InvalidTeamSizeError(
                "Player count must be divisible by team size and team size must be greater than 0")

        randomized_players = list(players)
        random.shuffle(randomized_players)
        random_teams = []

        for i in range(0, len(randomized_players), team_size):
            random_teams.append(randomized_players[i:i + team_size])
        return random_teams

    def teams_have_same_player(self, team_a_players, team_b_players):
        """Tarkistetaan onko sama pelaaja kahdessa joukkueessa.

        Args:
            team_a_players: Lista Player-olioita
            team_b_players: Lista Player-olioita

        Returns:
            True jos joukkueilla on sama pelaaja, muuten False
        """

        team_a_names = {player.name for player in team_a_players}
        team_b_names = {player.name for player in team_b_players}

        for name in team_a_names:
            if name in team_b_names:
                return True
        return False

    def update_player_ratings(self, team_a_players, team_b_players, team_a_won: bool):
        """Päivittää joukkeiden pelaajien ratingit.

        Args:
            team_a_players: Lista Player-olioita
            team_b_players: Lista Player-olioita
            team_a_won: Boolean-arvo, joka kertoo voittiko joukkue A
        """

        if self.teams_have_same_player(team_a_players, team_b_players):
            raise SamePlayerError("Teams cannot have the same player")

        team_a_average_rating = rating_service.calculate_team_average_rating(
            team_a_players)
        team_b_average_rating = rating_service.calculate_team_average_rating(
            team_b_players)

        team_a_expected_winratio = rating_service.calculate_expected_winratio(
            team_a_average_rating, team_b_average_rating)
        team_b_expected_winratio = rating_service.calculate_expected_winratio(
            team_b_average_rating, team_a_average_rating)

        team_a_score = 1 if team_a_won else 0
        team_b_score = 0 if team_a_won else 1

        for player in team_a_players:
            new_rating = rating_service.calculate_new_rating(
                player.rating, team_a_score, team_a_expected_winratio)
            self._player_repository.update_player_rating(player, new_rating)
            player.update_rating(new_rating)

        for player in team_b_players:
            new_rating = rating_service.calculate_new_rating(
                player.rating, team_b_score, team_b_expected_winratio)
            self._player_repository.update_player_rating(player, new_rating)
            player.update_rating(new_rating)

    def save_match_result(self, team_a_players, team_b_players, team_a_points, team_b_points):
        """Luo uuden pelin.

        Args:
            team_a_players: Lista Player-olioita
            team_b_players: Lista Player-olioita
            team_a_points: Lukuarvo, joka kertoo joukkueen A pisteet
            team_b_points: Lukuarvo, joka kertoo joukkueen B pisteet

        Returns:
            Match-olio: Luo uuden pelin
        """

        if self.teams_have_same_player(team_a_players, team_b_players):
            raise SamePlayerError("Teams cannot have the same player")
        team_a_player_names = [player.name for player in team_a_players]
        team_b_player_names = [player.name for player in team_b_players]
        match = Match(team_a_player_names, team_b_player_names, team_a_points, team_b_points)

        return self._match_repository.create(match)

    def get_all_matches(self):
        """Hakee kaikki pelit

        Returns:
            Lista Match-olioita, jotka on haettu tietokannasta
        """

        return self._match_repository.get_all_matches()

game_service = GameService()

class Match:
    """Luokka, joka määrittelee pelin

    Attributes:
        team_a_players: Lista pelaajista, jotka kuuluvat joukkueeseen A
        team_b_players: Lista pelaajista, jotka kuuluvat joukkueeseen B
        team_a_points: Joukkueen A pisteet
        team_b_points: Joukkueen B pisteet
        match_id: Pelin id tietokannassa
    """
    def __init__(
            self, team_a_players, team_b_players, team_a_points, team_b_points,
            *,  match_id=None
            ):
        """Luokan konstruktori, joka luo uuden pelin

        Args:
            team_a_players: Lista pelaajista, jotka kuuluvat joukkueeseen A
            team_b_players: Lista pelaajista, jotka kuuluvat joukkueeseen B
            team_a_points: Joukkueen A pisteet
            team_b_points: Joukkueen B pisteet
            match_id: Pelin id tietokannassa
        """
        self.id = match_id
        self.team_a_players = team_a_players
        self.team_b_players = team_b_players
        self.team_a_points = team_a_points
        self.team_b_points = team_b_points

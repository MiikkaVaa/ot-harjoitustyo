from ui.players_view import PlayersView
from ui.match_view import MatchView
from ui.match_history_view import MatchHistoryView

class UI:
    """Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, root):
        """Luokan konstruktori.

        Args:
            root: Tkinter-elementti, joka toimii sovelluksen juurielementtinä
        """

        self._root = root
        self._current_view = None

    def start(self):
        """Käynnistä käyttöliittymä.
        """

        self._show_players_view()

    def _hide_current_view(self):
        """Sulje nykyinen näkymä.
        """

        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_players_view(self):
        """Näytä pelaajien hallintaan liittyvä näkymä.
        """

        self._hide_current_view()
        self._current_view = PlayersView(self._root, self._show_match_view, self._show_match_history_view) #pylint: disable=too-many-function-args
        self._current_view.pack()

    def _show_match_view(self):
        """Näytä pelin tallentamiseen liittyvä näkymä.
        """

        self._hide_current_view()
        self._current_view = MatchView(self._root, self._show_players_view)
        self._current_view.pack()

    def _show_match_history_view(self):
        """Näytä pelihistorian tarkastelu näkymä
        """

        self._hide_current_view()
        self._current_view = MatchHistoryView(self._root, self._show_players_view)
        self._current_view.pack()

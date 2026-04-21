import tkinter as tk
from tkinter import ttk, messagebox, constants
from services.game_service import game_service, PlayerExistsError, InvalidPlayerNameError, InvalidTeamSizeError


class PlayersView:
    def __init__(self, root, handle_show_match_view):
        self._root = root
        self._handle_show_match_view = handle_show_match_view
        self._frame = None
        self._name_entry = None
        self._team_size_entry = None
        self._players_listbox = None
        self._teams_listbox = None
        self._players = []
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(self._root)

        title_label = ttk.Label(master=self._frame, text="Players")

        name_label = ttk.Label(master=self._frame, text="Player name")
        self._name_entry = ttk.Entry(master=self._frame)

        add_player_button = ttk.Button(
            master=self._frame, text="Add player", command=self._handle_add_player)

        players_label = ttk.Label(master=self._frame, text="All players")
        self._players_listbox = tk.Listbox(
            master=self._frame, height=12, selectmode=tk.MULTIPLE)

        title_label.grid(row=0, column=0, columnspan=2,
                         sticky=constants.W, padx=5, pady=5)
        name_label.grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        self._name_entry.grid(
            row=1, column=1, sticky=constants.EW, padx=5, pady=5)
        add_player_button.grid(row=2, column=0, columnspan=2,
                               sticky=constants.EW, padx=5, pady=5)
        players_label.grid(row=3, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        self._players_listbox.grid(
            row=4, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)

        self._frame.grid_columnconfigure(1, weight=1)

        team_size_label = ttk.Label(master=self._frame, text="Team size")
        self._team_size_entry = ttk.Entry(master=self._frame)
        create_teams_button = ttk.Button(
            master=self._frame, text="Randomizer", command=self._handle_create_teams,)

        teams_label = ttk.Label(master=self._frame, text="Teams")
        self._teams_listbox = tk.Listbox(master=self._frame, height=8)

        open_match_view_button = ttk.Button(
            master=self._frame, text="Record match result", command=self._handle_show_match_view
        )

        team_size_label.grid(row=5, column=0, sticky=constants.W, padx=5, pady=5)
        self._team_size_entry.grid(row=5, column=1, sticky=constants.EW, padx=5, pady=5)
        create_teams_button.grid(row=6, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)
        teams_label.grid(row=7, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)
        self._teams_listbox.grid(row=8, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)
        open_match_view_button.grid(
            row=9, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)

        self._load_players()

    def _get_selected_players(self):
        selected_players = self._players_listbox.curselection()
        return [self._players[i] for i in selected_players]

    def _handle_create_teams(self):
        selected_players = self._get_selected_players()
        try:
            team_size = int(self._team_size_entry.get())
            teams = game_service.create_random_teams(selected_players, team_size)
        except ValueError:
            messagebox.showerror(
                "Error", "Team size must be a whole number")
            return
        except InvalidTeamSizeError:
            messagebox.showerror(
                "Error", "Player count must be divisible by team size and team size must be greater than 0")
            return
 
        self._load_teams(teams)

    def _load_teams(self, teams):
        self._teams_listbox.delete(0, constants.END)
        for i, team in enumerate(teams, start=1):
            players_in_team = ", ".join(player.name for player in team)
            self._teams_listbox.insert(constants.END, f"Team {i}: {players_in_team}")

    def _handle_add_player(self):
        name = self._name_entry.get()
        try:
            game_service.create_player(name)
        except PlayerExistsError:
            messagebox.showerror(
                "Error", f"Player with name '{name}' already exists")
            return
        except InvalidPlayerNameError:
            messagebox.showerror("Error", "Player name cannot be empty")
            return

        self._name_entry.delete(0, constants.END)
        self._load_players()

    def _load_players(self):
        self._players = game_service.get_all_players()
        self._players_listbox.delete(0, constants.END)
        self._teams_listbox.delete(0, constants.END)
        for player in self._players:
            self._players_listbox.insert(
                constants.END, f"{player.name} (Rating: {player.rating})")

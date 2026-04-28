import tkinter as tk
from tkinter import ttk, constants
from services.game_service import game_service

class MatchHistoryView:
    def __init__(self, root, handle_show_players_view):
        self._root = root
        self._handle_show_players_view = handle_show_players_view
        self._frame = None
        self._matches_listbox = None
        self._team_a_players_label = None
        self._team_b_players_label = None
        self._team_a_points_label = None
        self._team_b_points_label = None
        self._matches = []
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(self._root)
        title_label = ttk.Label(master=self._frame, text = "Match History")
        list_label = ttk.Label(master=self._frame, text = "Matches")
        details_label = ttk.Label(master=self._frame, text = "Match Details")

        self._matches_listbox = tk.Listbox(
            master=self._frame,
            height = 12,
            selectmode = tk.SINGLE,
            exportselection=False)
        
        self._matches_listbox.bind("<<ListboxSelect>>", self._handle_match_select)
        self._team_a_players_label = ttk.Label(master=self._frame, text="Team A players: ")
        self._team_b_players_label = ttk.Label(master=self._frame, text="Team B players: ")
        self._team_a_points_label = ttk.Label(master=self._frame, text="Team A points: ")
        self._team_b_points_label = ttk.Label(master=self._frame, text="Team B points: ")

        back_button = ttk.Button(
            master=self._frame,
            text="Back",
            command=self._handle_show_players_view)

        title_label.grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)
        list_label.grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        details_label.grid(row=1, column=1, sticky=constants.W, padx=5, pady=5)

        self._matches_listbox.grid(row=2, column=0, rowspan=4, sticky=constants.NSEW, padx=5, pady=5)
        self._team_a_players_label.grid(row=2, column=1, sticky=constants.W, padx=5, pady=5)
        self._team_b_players_label.grid(row=3, column=1, sticky=constants.W, padx=5, pady=5)
        self._team_a_points_label.grid(row=4, column=1, sticky=constants.W, padx=5, pady=5)
        self._team_b_points_label.grid(row=5, column=1, sticky=constants.W, padx=5, pady=5)
        back_button.grid(row=6, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)

        self._load_matches()


    def _load_matches(self):
        self._matches = game_service.get_all_matches()
        self._matches_listbox.delete(0, constants.END)
        for match in self._matches:
            self._matches_listbox.insert(constants.END, f"Match {match.id}")

    def _handle_match_select(self, _event):
        selected_index_tuple = self._matches_listbox.curselection()
        if not selected_index_tuple:
            return
        selected_index = selected_index_tuple[0]
        match = self._matches[selected_index]
        team_a_players = ", ".join(match.team_a_players) if match.team_a_players else "No players"
        team_b_players = ", ".join(match.team_b_players) if match.team_b_players else "No players"
        self._team_a_players_label.config(text=f"Team A players: {team_a_players}")
        self._team_b_players_label.config(text=f"Team B players: {team_b_players}")
        self._team_a_points_label.config(text=f"Team A points: {match.team_a_points}")
        self._team_b_points_label.config(text=f"Team B points: {match.team_b_points}")

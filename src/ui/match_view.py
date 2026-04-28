import tkinter as tk
from tkinter import ttk, messagebox, constants
from services.game_service import game_service, SamePlayerError

class MatchView:
    def __init__(self, root, handle_show_players_view):
        self._root = root
        self._handle_show_players_view = handle_show_players_view
        self._frame = None
        self._team_a_listbox = None
        self._team_b_listbox = None
        self._team_a_points_entry = None
        self._team_b_points_entry = None
        self._players = []
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X, padx=10, pady=10)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(self._root)

        title_label = ttk.Label(master=self._frame, text="Match result")

        team_a_label = ttk.Label(master=self._frame, text="Team A")
        self._team_a_listbox = tk.Listbox(master=self._frame, height=8, selectmode=tk.MULTIPLE, export=False)

        team_b_label = ttk.Label(master=self._frame, text="Team B")
        self._team_b_listbox = tk.Listbox(master=self._frame, height=8, selectmode=tk.MULTIPLE, export=False)

        team_a_points_label = ttk.Label(master=self._frame, text="Team A points")
        self._team_a_points_entry = ttk.Entry(master=self._frame)

        team_b_points_label = ttk.Label(master=self._frame, text="Team B points")
        self._team_b_points_entry = ttk.Entry(master=self._frame)

        save_match_button = ttk.Button(master=self._frame, text="Save match result", command=self._handle_save_match)
        back_button = ttk.Button(master=self._frame, text="Back", command=self._handle_show_players_view)

        title_label.grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)

        team_a_label.grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        self._team_a_listbox.grid(row=2, column=0, sticky=constants.EW, padx=5, pady=5)

        team_b_label.grid(row=1, column=1, sticky=constants.W, padx=5, pady=5)
        self._team_b_listbox.grid(row=2, column=1, sticky=constants.EW, padx=5, pady=5)

        team_a_points_label.grid(row=3, column=0, sticky=constants.W, padx=5, pady=5)
        self._team_a_points_entry.grid(row=4, column=0, sticky=constants.EW, padx=5, pady=5)

        team_b_points_label.grid(row=3, column=1, sticky=constants.W, padx=5, pady=5)
        self._team_b_points_entry.grid(row=4, column=1, sticky=constants.EW, padx=5, pady=5)

        save_match_button.grid(row=5, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)
        back_button.grid(row=6, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)
        self._load_players()

    def _load_players(self):
        self._players = game_service.get_all_players()
        self._team_a_listbox.delete(0, tk.END)
        self._team_b_listbox.delete(0, tk.END)

        for player in self._players:
            self._team_a_listbox.insert(tk.END, player.name)
            self._team_b_listbox.insert(tk.END, player.name)

    def _get_selected_players(self, listbox):
        selected_indexes = listbox.curselection()
        return [self._players[i] for i in selected_indexes]

    def _handle_save_match(self):
        team_a_players = self._get_selected_players(self._team_a_listbox)
        team_b_players = self._get_selected_players(self._team_b_listbox)

        try:
            team_a_points = int(self._team_a_points_entry.get())
            team_b_points = int(self._team_b_points_entry.get())

        except ValueError:
            messagebox.showerror("Error", "Points must be integers")
            return

        team_a_won = team_a_points > team_b_points

        try:
            game_service.update_player_ratings(team_a_players, team_b_players, team_a_won)
            game_service.save_match_result(
                team_a_players, team_b_players, team_a_points, team_b_points
            )

        except SamePlayerError:
            messagebox.showerror("Error", "Teams cannot have the same player")
            return

        messagebox.showinfo("Match result saved and ratings updated", "Done")

        self._load_players()
        self._team_a_points_entry.delete(0, tk.END)
        self._team_b_points_entry.delete(0, tk.END)

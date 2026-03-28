import tkinter as tk
from tkinter import ttk, messagebox, constants
from services.game_service import game_service, PlayerExistsError, InvalidPlayerNameError

class PlayersView:
    def __init__(self, root):
        self._root = root
        self._frame = None
        self._name_entry = None
        self._players_listbox = None
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

        add_player_button = ttk.Button(master=self._frame, text="Add player", command=self._handle_add_player)

        players_label = ttk.Label(master=self._frame, text="All players")
        self._players_listbox = tk.Listbox(master=self._frame, height=20)

        title_label.grid(row=0, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)
        name_label.grid(row=1, column=0, sticky=constants.W, padx=5, pady=5)
        self._name_entry.grid(row=1, column=1, sticky=constants.EW, padx=5, pady=5)
        add_player_button.grid(row=2, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)
        players_label.grid(row=3, column=0, columnspan=2, sticky=constants.W, padx=5, pady=5)
        self._players_listbox.grid(row=4, column=0, columnspan=2, sticky=constants.EW, padx=5, pady=5)

        self._frame.grid_columnconfigure(1, weight=1)
        self._load_players()
    
    def _handle_add_player(self):
        name = self._name_entry.get()
        try:
            game_service.create_player(name)
        except PlayerExistsError:
            messagebox.showerror("Error", f"Player with name '{name}' already exists")
        except InvalidPlayerNameError:
            messagebox.showerror("Error", "Player name cannot be empty")
        
        self._name_entry.delete(0, constants.END)
        self._load_players()
    
    def _load_players(self):
        self._players_listbox.delete(0, constants.END)
        players = game_service.get_all_players()
        for player in players:
            self._players_listbox.insert(constants.END, f"{player.name} (Rating: {player.rating})")
        
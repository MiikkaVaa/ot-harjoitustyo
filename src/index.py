from tkinter import Tk
from ui.ui import UI
from initialize_database import ensure_database_initialized


def main():
    ensure_database_initialized()
    window = Tk()
    window.title("Megazone Rating")
    ui_view = UI(window)
    ui_view.start()
    window.mainloop()


if __name__ == "__main__":
    main()

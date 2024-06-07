import tkinter as tk
from appMenus import main_menu_appearance, first_window
if __name__ == "__main__":
    app_window = tk.Tk()
    main_menu_appearance(app_window, "MongoDB Helper")
    first_window(app_window)
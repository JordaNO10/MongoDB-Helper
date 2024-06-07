import tkinter as tk
from tkinter import Label, messagebox

from first_menu_selection import delete_collection_menu, add_records

app_window = tk.Tk()


def main_menu_appearance(window: tk.Tk, title: str) -> None:
    """
        Configures the appearance of the main menu window.

        Args:
            window (tk.Tk): The main menu window object.
            title (str): The title of the main menu window.

        Returns:
            None
        """
    window.title(f"{title}")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window.winfo_reqwidth() / 2))
    y_coordinate = int((screen_height / 2) - (window.winfo_reqheight() / 2))
    window.geometry(f"+{x_coordinate}+{y_coordinate}")
    window.resizable(False, False)
    app_window.withdraw()


def on_closing() -> None:
    """
    Close the application window.

    This function prompts the user with a messagebox to confirm if they want to quit the application.
    If the user clicks "OK", the application window is closed.

    Returns:
        None
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app_window.quit()
        app_window.destroy()


def first_window(window: tk.Tk) -> None:
    """
    Display the main menu window.

    This function creates the main menu window with buttons for adding records, deleting collections, and closing the application.

    Args:
        window (tk.Tk): The main application window.

    Returns:
        None
    """

    def records_add() -> None:
        """
        Switch to the add records menu.

        This function hides the current window, switches to the add records menu, and then restores the current window.

        Returns:
            None
        """
        window.withdraw()
        add_records()
        window.deiconify()

    def record_delete() -> None:
        """
        Switch to the delete collection menu.

        This function hides the current window, switches to the delete collection menu, and then restores the current window.

        Returns:
            None
        """
        window.withdraw()
        delete_collection_menu()
        window.deiconify()

    def app_close() -> None:
        """
        Close the application.

        This function triggers the application closing sequence.

        Returns:
            None
        """
        on_closing()

    add_records_button = tk.Button(window, text="Create Database & Collection \n Overwrite Collection",
                                   command=records_add, width=50)
    button_delete_collection = tk.Button(window, text="Delete Collection", command=record_delete, width=50)
    button_close_app = tk.Button(window, text="Exit", command=app_close, width=50)

    add_records_button.pack(pady=5)
    button_delete_collection.pack(pady=5)
    button_close_app.pack(pady=5)

    bottom_text = Label(window, text="Created By Yarden Halely\nVersion 2.0", pady=10)
    bottom_text.pack()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

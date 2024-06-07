import tkinter as tk
from tkinter import filedialog, messagebox
import json


def load_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str): The path to the JSON file to be loaded.

    Returns:
        list: A list of dictionaries representing the JSON data if the file is
        successfully loaded and contains valid JSON data.
        None: If the file cannot be loaded or does not contain valid JSON data.
    """
    try:
        with open(file_path, 'r') as Jsonfile:
            data = json.load(Jsonfile)
        if isinstance(data, list):
            return data
        else:
            print("Invalid JSON format. The JSON data must be a list of dictionaries.")
            return None
    except Exception as e:
        print(f"An error occurred while loading JSON: {e}")
        return None


def browse_json_file():
    """
    Open a file menu to select a JSON file.

    Returns:
        str: The file path of the selected JSON file if valid.
        None: If no file is selected / the selection is aborted, or if the selected
        file is not a valid JSON file.
    """
    while True:
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            parent=root,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        root.destroy()

        if not file_path:
            return None

        try:
            with open(file_path, 'r') as file:
                json.load(file)
            return file_path
        except Exception:
            messagebox.showerror("Invalid JSON",
                                 "The selected file is not a valid JSON file.\nPlease pick a different JSON file.")

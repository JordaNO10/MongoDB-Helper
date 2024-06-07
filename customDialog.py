import tkinter as tk
import typing


def create_custom_dialog(title: str, prompt: str) -> typing.Optional[str]:
    """
     Create a custom dialog window with a title, prompt, and an entry field.

     Args:
         title (str): The title of the dialog window.
         prompt (str): The prompt message displayed in the dialog window.

     Returns:
         str or None: The text entered by the user in the entry field when the OK button is clicked,
         or None if the dialog is closed without entering any text.

     Note:
         This function creates a custom dialog window using Tkinter's Toplevel widget. The dialog window
         contains a label with the provided prompt message and an entry field where the user can input text.
         The user can press the OK button to confirm their input, and the dialog window will be closed.
         Pressing the Enter key also triggers the OK button's action. If the user closes the dialog window
         without entering any text, the function returns None.

     """
    dialog = tk.Toplevel()
    dialog.title(title)

    # Prevent resizing of the dialog window
    dialog.resizable(False, False)

    # Center the dialog window
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2
    y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2
    dialog.geometry("+%d+%d" % (x, y))

    label = tk.Label(dialog, text=prompt)
    label.pack()

    entry_var = tk.StringVar()  # Variable to hold the entry value
    entry = tk.Entry(dialog, textvariable=entry_var)
    entry.pack()

    # Ensure focus is set to the entry field
    entry.focus_force()

    result = None  # Initialize result to handle Cancel button click

    def on_ok():
        nonlocal result
        result = entry_var.get()
        dialog.destroy()

    button_ok = tk.Button(dialog, text="OK", command=on_ok)
    button_ok.pack()

    # Bind the <Return> key to the OK button's action
    dialog.bind("<Return>", lambda event: on_ok())

    # Custom geometry for the dialog window
    dialog.geometry("350x150")

    # Wait for the dialog to close
    dialog.wait_window(dialog)

    return result

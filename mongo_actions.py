import json
import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, Scrollbar, Button, Label

import pymongo

from ImportantMassages import records_added_to_collection, collection_overwritten, not_exists, collection_deleted
from customDialog import create_custom_dialog
from filebrowse import load_json, browse_json_file

# Main actions of Tkinter to make everything easier
root = tk.Tk()
root.withdraw()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Calculate the x and y coordinates for the Tk root window to be centered
x_coordinate = (screen_width / 2) - (root.winfo_reqwidth() / 2)
y_coordinate = (screen_height / 2) - (root.winfo_reqheight() / 2)


def connect_to_mongodb() -> pymongo.MongoClient:
    """
       Connects to MongoDB.

       Returns:
           pymongo.MongoClient: The MongoDB client.

       Raises:
           ConnectionError: If an error occurs while connecting to MongoDB.
       """
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        return client
    except Exception as e:
        raise ConnectionError(f"An error occurred while connecting to MongoDB: {e}")


mongo_client = connect_to_mongodb()


def create_database():
    """
       Creates a new MongoDB database.

       Returns:
           str: The name of the newly created database, or None if the operation fails.
       """
    client = connect_to_mongodb()
    new_database_name = create_custom_dialog("Database name", "Enter New database name")
    if new_database_name:
        existing_databases = client.list_database_names()
        # Check if a similar database name already exists (case-insensitive)
        similar_database = next((db for db in existing_databases if db.lower() == new_database_name.lower()), None)
        if similar_database:
            messagebox.showwarning("Entering Database",
                                   f"A database named '{similar_database}' already exists.")
            messagebox.showwarning("Database selection", f"If you wish to overwrite the database {similar_database},\n"
                                                         f"Press it and you will continue "
                                                         f"to the collection overwrite/create screen")
            return None
        db = client[new_database_name]
        new_collection_name = create_custom_dialog("Enter Collection Name", "Enter Collection name")
        if new_collection_name:
            db[new_collection_name].insert_one({"new": "record"})
            return new_database_name
    return None


def select_database_screen() -> str:
    """
       Opens a new window with a list of database names for the user to select from.

       Returns:
           str: The name of the selected database.
       """

    def on_database_select(_event):
        # Get the selected database name
        selected_index = listbox.curselection()
        if selected_index:
            selected_db = listbox.get(selected_index)
            selection.set(selected_db)
            db_window.destroy()

    def create_new_database():
        new_db_name = create_database()
        if new_db_name:
            selection.set(new_db_name)
            db_window.destroy()

    # Create a new Toplevel window
    db_window = Toplevel()
    db_window.title("Select Database")

    # Set the position of the window
    window_width = 300
    window_height = 397
    db_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Prevent window resizing
    db_window.resizable(False, False)

    # List all databases
    database_names = connect_to_mongodb().list_database_names()
    filtered_database_names = [db for db in database_names if db not in {'local', 'admin', 'config'}]

    # Create a Listbox widget with a scrollbar
    scrollbar = Scrollbar(db_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(db_window, yscrollcommand=scrollbar.set)
    for db_name in filtered_database_names:
        listbox.insert(tk.END, db_name)
    listbox.pack(padx=20, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure scrollbar
    scrollbar.config(command=listbox.yview)

    # Add a label to display a selected database
    selection = tk.StringVar()
    selected_label = Label(db_window, textvariable=selection)
    selected_label.pack(pady=10)

    # Bind the double click event
    listbox.bind("<Double-1>", on_database_select)

    # Create Database button
    create_button = Button(db_window, text="Create Database", command=create_new_database)
    create_button.pack(side=tk.TOP, pady=10)

    # Main manu button
    main_manu_button = Button(db_window, text="Main Manu", command=db_window.destroy)
    main_manu_button.pack(side=tk.BOTTOM, pady=10)

    # Wait for the window to close
    db_window.wait_window()

    # Return the selected database name
    return selection.get()


def select_database_delete_screen() -> str:
    """
    Opens a new window with a list of database names for the user to select
    which to delete.

    Returns:
        str: The name of the selected database.
    """

    def on_database_select(_event):
        # Get the selected database name
        selected_index = listbox.curselection()
        if selected_index:
            selected_db = listbox.get(selected_index)
            selection.set(selected_db)
            pick_answer = tk.messagebox.askyesno("Database selected", f"Is this the database you meant to pick ?\n"
                                                                      f"{selected_db} ")
            if pick_answer:
                selection.set(selected_db)
                db_window.destroy()
            else:
                messagebox.showinfo("Select Database", "Please select a different database")

    # Create a new Toplevel window
    db_window = Toplevel()
    db_window.title("Select Database")

    # Set the position of the window
    window_width = 300
    window_height = 397
    db_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Prevent window resizing
    db_window.resizable(False, False)

    # List all databases
    database_names = connect_to_mongodb().list_database_names()
    filtered_database_names = [db for db in database_names if db not in {'local', 'admin', 'config'}]

    # Create a Listbox widget with a scrollbar
    scrollbar = Scrollbar(db_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(db_window, yscrollcommand=scrollbar.set)
    for db_name in filtered_database_names:
        listbox.insert(tk.END, db_name)
    listbox.pack(padx=20, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure scrollbar
    scrollbar.config(command=listbox.yview)

    # Add a label to display a selected database
    selection = tk.StringVar()
    selected_label = Label(db_window, textvariable=selection)
    selected_label.pack(pady=10)

    # Bind the double click event
    listbox.bind("<Double-1>", on_database_select)

    # Close button
    close_button = Button(db_window, text="Back", command=db_window.destroy)
    close_button.pack(side=tk.BOTTOM, pady=10)

    # Wait for the window to close
    db_window.wait_window()

    # Return the selected database name
    return selection.get()


def collection_select_screen(database_name: str) -> str:
    """
        Opens a selection window screen for the user to select
        from the database which collection to use.

        Args:
            database_name (str): The name of the database.

        Returns:
            str: The name of the selected collection.
        """

    def refresh_collection_menu():
        collection_names = mongo_client.get_database(database_name).list_collection_names()
        listbox.delete(0, tk.END)
        for col_name in collection_names:
            listbox.insert(tk.END, col_name)

    def add_new_collection():
        create_collection(database_name)
        refresh_collection_menu()

    def overwrite_existing_collection():
        try:
            selected_index = listbox.curselection()
            if selected_index:
                selected_collection = listbox.get(selected_index)
                overwrite_answer = messagebox.askyesno("Collection Not Empty",
                                                       f"Overwrite existing records at: '{selected_collection}'?")
                if overwrite_answer:
                    file_path = browse_json_file()
                    if file_path:
                        overwrite_collection(mongo_client, database_name, selected_collection, file_path)
                        messagebox.showinfo("Success",
                                            f"Collection '{selected_collection}' overwritten successfully!")
                        refresh_collection_menu()
                    else:
                        messagebox.showerror("Error", "No file selected.")
        except tk.TclError:
            messagebox.showerror("Error", "No collection selected. Please select a collection from the list.")

    def close_window():
        col_window.destroy()

    # Create a new Toplevel window
    col_window = Toplevel()
    col_window.title("Select Collection")

    # Set the position of the window
    window_width = 300
    window_height = 397
    col_window.resizable(False, False)
    col_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Create a Listbox widget with a scrollbar
    scrollbar = Scrollbar(col_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(col_window, yscrollcommand=scrollbar.set)
    refresh_collection_menu()  # Initial population of the listbox
    listbox.pack(padx=20, pady=20)

    # Configure scrollbar
    scrollbar.config(command=listbox.yview)

    # Add a label to display a selected collection
    selection = tk.StringVar()
    selected_label = Label(col_window, textvariable=selection)
    selected_label.pack(pady=10)

    # Add new collection button
    add_collection_button = Button(col_window, text="Add New Collection", command=add_new_collection)
    add_collection_button.pack(pady=5)

    # Overwrite button
    overwrite_collection_button = Button(col_window, text="Overwrite Existing Collection",
                                         command=overwrite_existing_collection)
    overwrite_collection_button.pack(pady=5)

    # Main menu button
    main_menu_button = Button(col_window, text="Main Menu", command=close_window)
    main_menu_button.pack(side=tk.BOTTOM, pady=10)

    # Wait for the window to close
    col_window.wait_window()

    # Return the selected collection name
    return selection.get()


def create_collection(db_name: str):
    """
    Creates a new collection in the selected database.

    Args:
        db_name (str): The name of the database.

    Raises:
        ValueError: If the collection name is empty.
    """
    new_collection_name = create_custom_dialog("Collection name", "Enter New Collection name")
    if new_collection_name:
        db = mongo_client.get_database(db_name)
        if new_collection_name in db.list_collection_names():
            answer = messagebox.askyesno("Collection Exists",
                                         f"A collection named '{new_collection_name}' already exists."
                                         f"\nDo you wish to overwrite it?")
            if answer:
                file_path = browse_json_file()
                if file_path:
                    overwrite_collection(mongo_client, db_name, new_collection_name, file_path)
                else:
                    messagebox.showerror("Error", "No file selected.")
        else:
            file_path = browse_json_file()
            if file_path:
                records = load_json(file_path)
                if records:
                    add_collection(mongo_client, db_name, new_collection_name, records)
                else:
                    messagebox.showerror("Error", "Records must be a non-empty list.")
            else:
                messagebox.showerror("Error", "No file selected.")
    else:
        messagebox.showwarning("No Collection Name", "Collection name cannot be empty.")


def overwrite_collection(client, database_name: str, collection_name: str, file_path: str):
    """
    Overwrites an existing collection with records from a JSON file.

    Args:
        client: The MongoDB client.
        database_name (str): The name of the database.
        collection_name (str): The name of the collection.
        file_path (str): The path to the JSON file.

    Raises:
        ValueError: If database_name or collection_name is not a string,
                    or if records in the JSON file are not in a list format.
    """
    try:
        # Ensure the database and collection names are strings
        if not isinstance(database_name, str):
            raise ValueError("Database name must be a string")
        if not isinstance(collection_name, str):
            raise ValueError("Collection name must be a string")

        db = client[database_name]

        # Drop the existing collection if it exists
        if collection_name in db.list_collection_names():
            db.drop_collection(collection_name)

        # Create new collection and insert records
        collection = db[collection_name]
        with open(file_path, 'r') as file:
            new_records = json.load(file)
        if not isinstance(new_records, list):
            raise ValueError("Records must be a list")
        records_added = collection.insert_many(new_records)
        collection_overwritten(len(records_added.inserted_ids), collection_name, database_name)
    except Exception as e:
        print(f"An error occurred while overwriting collection in MongoDB: {e}")


def add_collection(client, database_name: str, collection_name: str, records: list):
    """
    Adds records to a collection in the specified database.

    Args:
        client: The MongoDB client.
        database_name (str): The name of the database.
        collection_name (str): The name of the collection.
        records (list): The records to add to the collection.

    Raises:
        ValueError: If database_name or collection_name is not a string,
                    or if records is not a non-empty list.
    """
    try:
        # Ensure the database and collection names are strings
        if not isinstance(database_name, str):
            raise ValueError("Database name must be a string")
        if not isinstance(collection_name, str):
            raise ValueError("Collection name must be a string")
        if not isinstance(records, list) or not records:
            raise ValueError("Records must be a non-empty list")

        db = client[database_name]
        collection = db[collection_name]
        records_added = collection.insert_many(records)
        records_added_to_collection(len(records_added.inserted_ids), collection_name, database_name)
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred while adding records to MongoDB: {e}")


def delete_collection(client, db_name: str, collection_name: str):
    """
    Deletes a collection from the selectd database.

    Args:
        client: The MongoDB client.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection to delete.

    Raises:
        ValueError: If db_name or collection_name is not a string.
    """
    try:
        db = client[db_name]
        if collection_name in db.list_collection_names():
            db.drop_collection(collection_name)
            collection_deleted(collection_name)
        else:
            not_exists(collection_name, db_name)
    except Exception as e:
        print(f"An error occurred while deleting collection from MongoDB: {e}")


def delete_collection_screen(database_name: str):
    """
    Opens a window to select and delete a collection from the selected database.

    Args:
        database_name (str): The name of the database.

    Returns:
        str: The name of the selected collection to delete.
    """
    messagebox.showwarning("Caution", "Be aware You now entering The deletion Screen"
                                      "\n if you got here by mistake press "
                                      "the 'Main Menu' at the bottom screen")

    def on_collection_select(_event):
        # Get the selected collection name
        selected_index = listbox.curselection()
        if selected_index:
            selected_collection = listbox.get(selected_index)
            collection = mongo_client.get_database(database_name)[selected_collection]
            if collection.count_documents({}) > 0:
                delete_answer = messagebox.askyesno("Records Found",
                                                    f"The selected collection is: '{selected_collection}'\n"
                                                    f"Do you wish to delete it?")
                if delete_answer:
                    delete_collection(mongo_client, database_name, selected_collection)
                    refresh_collection_menu()  # Refresh the collection menu after deletion

                    # Check if there are no collections left
                    if not mongo_client.get_database(database_name).list_collection_names():
                        messagebox.showinfo("No Collections Left", "No collections left, returning to main menu")
                        col_window.destroy()
            else:
                delete_collection(mongo_client, database_name, selected_collection)
                refresh_collection_menu()  # Refresh the collection menu after deletion
                # Check if there are no collections left
                if not mongo_client.get_database(database_name).list_collection_names():
                    messagebox.showinfo("No Collections Left", "No collections left, returning to main menu")
                    col_window.destroy()

    def close_window():
        col_window.destroy()

    def refresh_collection_menu():
        # Get the list of collection names and update the Listbox
        collection_names = mongo_client.get_database(database_name).list_collection_names()
        listbox.delete(0, tk.END)
        for col_name in collection_names:
            listbox.insert(tk.END, col_name)

    # Create a new Toplevel window
    col_window = Toplevel()
    col_window.title("Select Collection")

    # Set the position and size of the window
    window_width = 300
    window_height = 397
    col_window.resizable(False, False)
    width = (col_window.winfo_screenwidth() // 2) - (window_width // 2)
    height = (col_window.winfo_screenheight() // 2) - (window_height // 2)
    col_window.geometry(f"{window_width}x{window_height}+{width}+{height}")

    # List all collections in the selected database
    collection_names = mongo_client.get_database(database_name).list_collection_names()

    # Create a Listbox widget with a scrollbar
    scrollbar = Scrollbar(col_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(col_window, yscrollcommand=scrollbar.set)
    for col_name in collection_names:
        listbox.insert(tk.END, col_name)
    listbox.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Configure scrollbar
    scrollbar.config(command=listbox.yview)

    # Add a label to display a selected collection
    selection = tk.StringVar()
    selected_label = Label(col_window, textvariable=selection)
    selected_label.pack(pady=10)

    # Delete Button
    delete_button = Button(col_window, text="Delete Collection", command=lambda: on_collection_select(listbox))
    delete_button.pack(side=tk.TOP, padx=50, pady=10, fill=tk.BOTH)

    # Close button
    main_menu_button = Button(col_window, text="Main Menu", command=close_window)
    main_menu_button.pack(pady=10)

    # Wait for the window to close
    col_window.wait_window()

    return selection.get()

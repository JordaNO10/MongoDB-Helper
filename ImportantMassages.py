from tkinter import messagebox


def records_added_to_collection(records: int, collection: str, database: str):
    """
    Display a messagebox indicating the successful addition of records to a collection.

    Args:
        records (int): The number of records added.
        collection (str): The name of the collection.
        database (str): The name of the database.
    """
    records_added = (
        "Success!\n"
        f"{records} Records were added To :\n "
        f"{collection} Collection in :\n"
        f"{database} Database\n"
    )
    messagebox.showinfo("Json Import - Successful", records_added)


def database_already_created(database: str):
    """
    Display a messagebox indicating that the database is already created.

    Args:
        database (str): The name of the database.
    """
    has_records = (
        f"{database} Database - already Created,\n"
        "Please Start the program again and\n"
        "Change your Database name"
    )
    messagebox.showerror("Database Already Created", has_records)


def collection_overwritten(records: int, collection: str, database: str):
    """
    Display a messagebox indicating the successful overwrite of a collection.

    Args:
        records (int): The number of records overwritten.
        collection (str): The name of the collection.
        database (str): The name of the database.
    """
    records_added = (
        "Success!\n"
        f"{records} Records were Overwritten In :\n "
        f"{collection} Collection in the :\n"
        f"{database} Database\n"
    )
    messagebox.showinfo("Json Import - Successful", records_added)


def collection_already_exists(collection_name: str, database_name: str):
    """
    display a messagebox indicating that the collection already exists.

    Args:
        collection_name (str): The name of the collection.
        database_name (str): The name of the database.
    """
    already_exists = (
        f"{collection_name} Collection - already Exists\n"
        f"in  {database_name}"
        "Please Try a different name"
    )
    messagebox.showerror("Database Already Exists", already_exists)


def not_exists(collection_name: str, database_name: str):
    """
    Display a messagebox indicating that the collection does not exist.

    Args:
        collection_name (str): The name of the collection.
        database_name (str): The name of the database.
    """
    collection_not_exist = (
        f"{collection_name} Collection - does not Exist\n"
        f"in {database_name}"
        "Please check your Collection name"
    )
    messagebox.showerror("Collection Does Not Exist", collection_not_exist)


def collection_deleted(collection: str):
    """
    Display a messagebox indicating the successful deletion of a collection.

    Args:
        collection (str): The name of the collection.
    """
    Collection_deleted = (
        "Success!\n"
        f"{collection} Collection Has Been Deleted Successfully\n "
    )
    messagebox.showinfo("Collection Deletion", Collection_deleted)

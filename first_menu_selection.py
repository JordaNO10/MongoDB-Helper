from mongo_actions import connect_to_mongodb, add_collection, \
    select_database_screen, collection_select_screen, delete_collection, delete_collection_screen, \
    select_database_delete_screen
from filebrowse import browse_json_file, load_json


def add_records():
    """
    Add records to a MongoDB collection.
    """
    database_name = select_database_screen()
    if database_name:
        collection_name = collection_select_screen(database_name)
        if collection_name:
            file_path = browse_json_file()
            if file_path:
                json_data = load_json(file_path)
                if json_data:
                    mongo_connect = connect_to_mongodb()
                    add_collection(mongo_connect, database_name, collection_name, json_data)


def delete_collection_menu():
    """
    Delete a collection from a MongoDB database.
    """
    database_name = select_database_delete_screen()
    if database_name:
        collection_name = delete_collection_screen(database_name)
        if collection_name:
            mongo_connect = connect_to_mongodb()
            delete_collection(mongo_connect, database_name, collection_name)

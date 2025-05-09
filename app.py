from mongo_manager import MongoManager
from dotenv import load_dotenv
import os

load_dotenv()
#print("MONGO_URI from .env :", os.getenv("MONGO_URI"))

uri = os.getenv("MONGO_URI")

if __name__ == "__main__":
    db_manager = MongoManager(uri=uri)
    
    print("Bases de données disponibles :")
    print(db_manager.list_databases())

    db_manager.db = "TP"
    print(f"Collections dans TP : {db_manager.list_collections()}")

    """
    db_manager.collection = "users"
    # Create a single document
    document = {
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com"
    }
    created_one = db_manager.create_one_document(document)
    print("\ncreate_one_document:", created_one)

    # Create multiple documents
    documents = [
        {"name": "Jane Doe", "age": 25, "email": "jane.doe@example.com"},
        {"name": "Alice", "age": 28, "email": "alice@example.com"},
        {"name": "Bob", "age": 30, "email": "bob@example.com"}
    ]
    created_many = db_manager.create_many_documents(documents)
    print("\ncreate_many_documents:", created_many)
    """

    db_manager.close_connection()

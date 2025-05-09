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

    db_manager.close_connection()

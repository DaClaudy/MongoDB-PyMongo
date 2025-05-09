from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.database import Database

class MongoManager:
    def __init__(self, uri: str, db_name: str = None, coll_name: str = None):
        self.__client = MongoClient(uri, server_api=ServerApi('1'), tls=True)
        try:
            ping = self.__client.admin.command({'ping': 1})
            print(f"Pinged your deployment: {ping}. You successfully connected to MongoDB!")
        except Exception as e:
            raise Exception("Unable to connect to MongoDB due to the following error:", str(e))
        
        self.__db: Database = None
        self.__collection: Collection = None

        if db_name:
            self.db = db_name
        if coll_name:
            self.collection = coll_name

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, db_name: str):
        self.__db = self.__client[db_name]
        print(f"Database set to: {db_name}")
        self.__collection = None

    @property
    def collection(self):
        return self.__collection

    @collection.setter
    def collection(self, coll_name: str):
        if self.db is None:
            raise Exception("Set the database before setting the collection.")
        self.__collection = self.db[coll_name]
        print(f"Collection set to: {coll_name}")

    def close_connection(self):
        self.__client.close()
        print("Connection closed.")

    def list_databases(self):
        try:
            return self.__client.list_database_names()
        except Exception as e:
            raise Exception("Unable to list the databases:", str(e))

    def list_collections(self):
        if self.db is not None:
            try:
                return self.db.list_collection_names()
            except Exception as e:
                raise Exception("Unable to list the collections:", str(e))
        else:
            raise Exception("Database not selected.")
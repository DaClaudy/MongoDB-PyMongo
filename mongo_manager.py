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
    def client(self):
        return self.__client
    
    @client.setter
    def client(self, value):
        self.__client = value

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
        
    def set_collection(self, collection_name):
        self.collection = self.client[self.db][collection_name]

        
    def create_one_document(self, document: dict):
        if self.collection is None:
            raise Exception("Collection not selected.")
        try:
            insert_result = self.collection.insert_one(document)
            return {
                "acknowledged": insert_result.acknowledged,
                "insertedId": str(insert_result.inserted_id)
            }
        except Exception as e:
            raise Exception("Unable to insert the document due to the following error: " + str(e))

    def create_many_documents(self, documents: list[dict]):
        if self.collection is None:
            raise Exception("Collection not selected.")
        try:
            insert_result = self.collection.insert_many(documents)
            return {
                "acknowledged": insert_result.acknowledged,
                "insertedIds": [str(_id) for _id in insert_result.inserted_ids]
            }
        except Exception as e:
            raise Exception("Unable to insert the documents due to the following error: " + str(e))
        
    def update_one_document(self, query: dict, new_values: dict):
        try:
            update_result = self.collection.update_one(query, new_values)
            return {
                "acknowledged": update_result.acknowledged,
                "insertedId": update_result.upserted_id,
                "matchedCount": update_result.matched_count,
                "modifiedCount": update_result.modified_count,
            }
        except Exception as e:
            raise Exception("Unable to update the document due to the following error:", str(e))

    def update_many_documents(self, query: dict, new_values: dict):
        try:
            update_result = self.collection.update_many(query, new_values)
            return {
                "acknowledged": update_result.acknowledged,
                "insertedId": update_result.upserted_id,
                "matchedCount": update_result.matched_count,
                "modifiedCount": update_result.modified_count,
            }
        except Exception as e:
            raise Exception("Unable to update the documents due to the following error:", str(e))
        
    def read_one_document(self, query: dict):
        try:
            document = self.collection.find_one(query)
            return document
        except Exception as e:
            raise Exception("Unable to read the document due to the following error:", str(e))

    def read_many_documents(self, query: dict):
        try:
            documents = self.collection.find(query)
            return list(documents)
        except Exception as e:
            raise Exception("Unable to read the documents due to the following error:", str(e))

    def delete_one_document(self, query: dict):
        try:
            delete_result = self.collection.delete_one(query)
            return {"acknowledged": delete_result.acknowledged, "deletedCount": delete_result.deleted_count}
        except Exception as e:
            raise Exception("Unable to delete the document due to the following error:", str(e))

    def delete_many_documents(self, query: dict):
        try:
            delete_result = self.collection.delete_many(query)
            return {"acknowledged": delete_result.acknowledged, "deletedCount": delete_result.deleted_count}
        except Exception as e:
            raise Exception("Unable to delete the documents due to the following error:", str(e))
        
    def close_connection(self):
        self.__client.close()
        print("Connection closed.")

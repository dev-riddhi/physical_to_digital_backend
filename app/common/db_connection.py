from pymongo import MongoClient
import os
from dotenv import load_dotenv


class Database:
    _client: MongoClient
    _db_name: str
    _db_uri: str

    def __init__(self):
        load_dotenv()
        self._db_name = os.getenv("DB_NAME")
        self._db_uri = os.getenv("DB_URI")

    def connectDB(self, collection: str):
        if collection == "users":
            self._client = MongoClient(self._db_uri)
            return self._client[self._db_name][collection]
        elif collection == "history":
            self._client = MongoClient(self._db_uri)
            return self._client[self._db_name][collection]
        elif collection == "images":
            pass
        elif collection == "analysis":
            pass

    def closeDB(self):
        self._client.close()

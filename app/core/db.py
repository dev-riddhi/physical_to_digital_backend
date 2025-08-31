from pymongo import MongoClient
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class DBCollections(Enum):
    USERS = "users"
    HISTORY = "history"

class Database:
    _client : MongoClient
    _db_name : str
    _db_uri : str
    def __init__(self):
        self._db_name = os.getenv("DB_NAME")
        self._db_uri = os.getenv("DB_URI")
    

    @classmethod
    def connectDB(self,db_collection: DBCollections):
        if DBCollections.USERS == db_collection:
            self._client = MongoClient(self._db_uri)
            return self._client[self._db_name][db_collection.USERS.value]
        else:
            self._client = MongoClient(self._db_uri)
            return self._client[self._db_name][db_collection.HISTORY.value]
        
    @classmethod
    def closeDB(self):
        self._client.close()
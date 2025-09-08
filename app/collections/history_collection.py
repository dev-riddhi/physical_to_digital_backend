from app.models.db_model import History
from app.common.db_connection import Database
from bson.objectid import ObjectId


class HistoryCollection:
    def __init__(self):
        self._collectio_name = "history"
        try:
            self._database = Database()
            self._collection = self._database.connectDB(self._collectio_name)
        except:
            pass

    def create_history(self, history: History):
        return self._collection.insert_one(history.dict())

    def read_history(self, id: str):
        return self._collection.find_one({"_id": ObjectId(id)})

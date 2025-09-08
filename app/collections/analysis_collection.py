from app.common.db_connection import Database
from app.models.db_model import Analysis


class AnalysisCollection:
    def __init__(self):
        self._collectio_name = "analysis"
        try:
            self._database = Database()
            self._collection = self._database.connectDB(self._collectio_name)
        except:
            pass

    def create_data(self, data: Analysis):
        return self._collection.insert_one(data.dict())

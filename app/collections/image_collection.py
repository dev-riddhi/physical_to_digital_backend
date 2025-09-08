from app.common.db_connection import Database
from app.models.db_model import Image
from bson.objectid import ObjectId


class ImageCollections:

    def __init__(self):
        self._collectio_name = "images"
        try:
            self._database = Database()
            self._collection = self._database.connectDB(self._collectio_name)
        except:
            pass

    def insert_image(self, image_info: Image):
        return self._collection.insert_one(image_info.dict())

    def read_image(self, id: str):
        return self._collection.find_one({"_id": ObjectId(id)})

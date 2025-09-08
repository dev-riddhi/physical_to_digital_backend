from app.models.db_model import Guest
from app.common.db_connection import Database


class GuestCollection:
    def __init__(self):
        self._collectio_name = "guest"
        try:
            self._database = Database()
            self._collection = self._database.connectDB(self._collectio_name)
        except:
            pass

    def create_guest(self, guest: Guest):
        return self._collection.insert_one(guest.dict())

    def read_guest(self, refresh_token: str):
        return self._collection.find_one({"refresh_token": refresh_token})

    def update_guest(self, refresh_token: str, guest: Guest):
        return self._collection.update_one(
            {"refresh_token": refresh_token}, {"$set": guest.dict()}
        )

    def update_limit(self, refresh_token: str, limit: int):
        return self._collection.update_one(
            {"refresh_token": refresh_token}, {"$set": {"limit": limit}}
        )

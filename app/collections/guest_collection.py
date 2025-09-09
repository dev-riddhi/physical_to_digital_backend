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

    def read_guest(self, access_token: str):
        return self._collection.find_one({"access_token": access_token})

    def update_guest_token(self, access_token: str, new_access_token: str):
        return self._collection.update_one(
            {"access_token": access_token}, {"$set": {"access_token": new_access_token}}
        )

    def update_guest(self, access_token: str, guest: Guest):
        return self._collection.update_one(
            {"access_token": access_token}, {"$set": guest.dict()}
        )

    def update_limit(self, access_token: str, limit: int):
        return self._collection.update_one(
            {"access_token": access_token}, {"$set": {"limit": limit}}
        )

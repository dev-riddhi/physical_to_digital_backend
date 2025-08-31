from app.common.db_connection import Database
from app.models.db_model import User

class UserCollection:

    # ======== init ============

    def __init__(self):
        self._collectio_name = "users"
        try:
            self._database = Database()
            self._collection = self._database.connectDB(self._collectio_name)
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    




    # ========== auth ===========
    
    def find_user(self,email : str):
        return self._collection.find_one({"email": email})
    
    def update_token(self,email:str,new_token:str):
        return self._collection.update_one({"email": email}, {"$set": {"token":new_token}})
    
    def remove_token(self,token:str):
        return self._collection.update_one({"token": token}, {"$set": {"token":""}})
    
    ## ============= auth end ===============














    ## ============= crud ====================
    
    def get_user(self,token: str):
        return self._collection.find_one({"token": token})

    def create_user(self,user_data : User):
        return self._collection.insert_one(user_data.dict())

    def update_user(self,email: str, update_data: User):
        return self._collection.update_one({"email": email}, {"$set": update_data.dict()}) 

    def delete_user(self,token: str):
        return self._collection.delete_one({"token": token})
    
    ## =============== crud end ==================
      








    # ================ extra ====================
    
    def __del__(self):
        self._database.closeDB()
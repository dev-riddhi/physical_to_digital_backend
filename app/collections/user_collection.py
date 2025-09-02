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

    # ======== init end ===========



    # ========== auth ===========
    
    def find_user(self,email : str):
        return self._collection.find_one({"email": email})
    
    def update_tokens_by_email(self,email:str,new_refresh_token:str,new_access_token:str):
        return self._collection.update_one({"email":email},{"$set" : {"refresh_token" : new_refresh_token,"access_token":new_access_token}})
    
    def verify_access(self,access_token:str):
        return self._collection.find_one({"access_token" : access_token})
    
    def update_refresh_token(self,old_refresh_token:str,new_refresh_token:str):
        return self._collection.update_one({"refresh_token": old_refresh_token}, {"$set": {"refresh_token":new_refresh_token}})
    
    def update_access_token(self,refresh_token:str,new_access_token:str):
        return self._collection.update_one({"refresh_token": refresh_token}, {"$set": {"access_token":new_access_token}})
    
    def remove_all_tokens(self,refresh_token:str):
        return self._collection.update_one({"refresh_token": refresh_token}, {"$set": {"refresh_token":"","access_token":""}})
    
    def check_refresh_token(self,refresh_token:str):
        return self._collection.find_one({"refresh_token":refresh_token})
    ## ============= auth end ===============






    ## ============= crud ====================
    
    def read_user(self,access_token: str):
        return self._collection.find_one({"access_token": access_token})

    def create_user(self,user_data : User):
        return self._collection.insert_one(user_data.dict())

    def update_user(self,access_token:str, update_data: User):
        return self._collection.update_one({"access_token": access_token}, {"$set": update_data.dict()}) 

    def delete_user(self,email: str, password:str):
        return self._collection.delete_one({"email": email,password:str})
    
    ## =============== crud end ==================
      








    # ================ extra ====================
    
    def close_connection(self):
        self._database.closeDB()
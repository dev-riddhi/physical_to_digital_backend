import datetime
from bson.objectid import ObjectId
class User():
    
    def __init__(self,name: str,email: str,password: str,created_at:datetime,type: str,access_token: str,refresh_token:str):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.type = type
        self.access_token = access_token
        self.refresh_token = refresh_token

    def dict(self):
        data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "type": self.type ,
            "access_token": self.access_token,
            "refresh_token" : self.refresh_token
        }

        return data

class History():
    user_id: ObjectId
    title: str
    creation_data: str
    images: list[str]

    def dict(self):
        return {
            "user_id": self.user_id,
            "creation_data": self.creation_data,
            "title": self.title,
            "images": self.images,
        }


class Images():
    user_id: ObjectId
    image_url: str
    uploaded_at: datetime

    def dict(self):
        return {}


class Analysis():
    total_visiters: int
    total_images: int
    recorded_date : datetime

    def dict(self):
        return {}
import datetime

class User():
    
    def __init__(self,name: str,email: str,password: str,type: str,token: str):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now()
        self.type = type
        self.token = token

    def dict(self):
        data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "type": self.type ,
            "token": self.token,
        }

        return data

class History():
    user_id: str
    images: list[str]
    timestamp: str
    details: str


class UploadedImage():
    user_id: str
    image_url: str
    uploaded_at: str


class Analysis():
    visiters: int
    total_images: int
    active_users: int

import datetime
from bson.objectid import ObjectId


class User:

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        created_at: datetime,
        type: str,
        history: list[ObjectId],
        access_token: str,
        refresh_token: str,
    ):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.type = type
        self.history = history
        self.access_token = access_token
        self.refresh_token = refresh_token

    def dict(self):
        data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "type": self.type,
            "history": self.history,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }

        return data


class History:

    def __init__(self, title: str, creation_data: str, images: list[ObjectId]):
        self.title = title
        self.creation_data = creation_data
        self.images = images

    def dict(self):
        return {
            "user_id": self.user_id,
            "creation_data": self.creation_data,
            "title": self.title,
            "images": self.images,
        }


class Image:

    def __init__(
        self,
        user_id: ObjectId,
        image_path: str,
        uploaded_at: datetime,
    ):
        self.user_id = user_id
        self.image_path = image_path
        self.uploaded_at = uploaded_at

    def dict(self):
        return {
            "user_id": self.user_id,
            "image_path": self.image_path,
            "uploaded_at": self.uploaded_at,
        }


class Analysis:
    def __init__(
        self,
        total_visiters: int,
        total_images: int,
        recorded_date: datetime,
    ):
        self.total_visiters = total_visiters
        self.total_images = total_images
        self.recorded_date = recorded_date

    def dict(self):
        return {
            "total_visiters": self.total_visiters,
            "total_images": self.total_images,
            "recorded_date": self.recorded_date,
        }


class Guest:
    def __init__(self, ip: str, limit: int, refresh_token: str, access_token: str):
        self.ip = ip
        self.limit = limit
        self.refresh_token = refresh_token
        self.access_token = access_token

    def dict(self):
        return {
            "ip": self.ip,
            "limit": self.limit,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
        }

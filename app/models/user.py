from pydantic import BaseModel, EmailStr
from enum import Enum

class UserType(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(BaseModel):
    name : str
    email: EmailStr
    password: str
    created_at : str
    type : UserType
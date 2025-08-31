from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str

class Signup(BaseModel):
    name: str
    email: EmailStr
    password: str
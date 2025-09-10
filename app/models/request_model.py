from pydantic import BaseModel


class UpdateUser(BaseModel):
    name: str
    email: str
    old_password: str
    new_password: str


class DeleteUser(BaseModel):
    password: str

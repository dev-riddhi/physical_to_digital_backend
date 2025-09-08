from pydantic import BaseModel


class UpdateUser(BaseModel):
    name: str | None = None
    email: str | None = None
    old_password: str | None = None
    new_password: str | None = None


class DeleteUser(BaseModel):
    password: str

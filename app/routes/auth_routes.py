from fastapi import APIRouter, Response, Cookie, Header
from app.models.auth_model import Login, Signup, Logout
from app.collections.user_collection import UserCollection
from app.models.db_model import User
from app.common.token_genarator import generate_token
from app.common.response_structure import (
    error_response,
    success_response,
    custom_response,
)
from enum import Enum
from datetime import datetime


class UserType(Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"


auth = APIRouter(
    prefix="/api",
)


@auth.post("/access")
def access_route(access_token: str = Header(default=None)):
    user_collection = UserCollection()

    new_access_token = generate_token(128)

    if not user_collection.verify_access_token_and_update(
        access_token, new_access_token
    ):
        return error_response(message="Unauthorised Access", code=98765432)

    return custom_response(
        message="success", code=987654, data={"access_token": new_access_token}
    )


@auth.post("/login")
def login_route(
    request: Login,
):

    user_collection = UserCollection()

    user = user_collection.find_user(request.email)

    if not user:
        return {"message": "email error"}

    if user["password"] != request.password:
        return {"message": "password error"}

    access_token = generate_token(128)

    if not user_collection.update_token_by_email(request.email, access_token):
        return {"message": "Unable to login"}

    user_collection.close_connection()

    return custom_response(
        message="Login success fully",
        code=87654,
        data={"access_token": access_token, "user_type": user["type"]},
    )


@auth.post("/signup")
def signup_route(request: Signup):

    user_collection = UserCollection()

    if user_collection.find_user(request.email):
        return {"message": "email is already used"}

    access_token = generate_token(128)

    new_user = User(
        name=request.name,
        email=request.email,
        password=request.password,
        type=UserType.USER.value,
        access_token=access_token,
        created_at=datetime.now(),
        history=[],
    )

    if not user_collection.create_user(new_user):
        return {"message": "Unable to create user | db error"}

    user_collection.close_connection()

    return custom_response(
        message="Login success fully",
        code=87654,
        data={"access_token": access_token, "user_type": UserType.USER.value},
    )


@auth.post("/logout")
def logout_route(refresh_token: str | None = Header(default=None)):

    user_collection = UserCollection()

    if not user_collection.check_refresh_token(refresh_token):
        return {"message": "Can't Logout"}

    if not user_collection.remove_all_tokens(refresh_token):
        return {"message": "unauthorised access"}

    user_collection.close_connection()

    return {"message": "Logout successful"}

from fastapi import APIRouter , Header
from app.models.auth_model import Login, Signup, Logout
from app.collections.user_collection import UserCollection
from app.models.db_model import User
from app.common.token_genarator import generate_token
from typing import Annotated
from enum import Enum

class UserType(Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"

auth = APIRouter(
    prefix="/api",
)

@auth.post("/login")
def login_route(request : Login):

    user_collection = UserCollection()
    user = user_collection.find_user(request.email)

    if not user:
        return {"message": "email error"}
    
    if  user['password'] != request.password :
        return {"message": "password error"}
    
    token = generate_token()

    if not user_collection.update_token(request.email,token):
        return {"message" : "Unable to login"}
    
    return {"token": token}
    

@auth.post("/signup")
def signup_route(request : Signup):

    user_collection = UserCollection()

    if user_collection.find_user(request.email):
        return {"message": "email is already used"}
    
    token = generate_token()

    new_user = User(
        name=request.name,
        email=request.email,
        password=request.password,
        type=UserType.USER.value,
        token=token
    )
    
    if(not user_collection.create_user(new_user)):
        return {
            "message" : "Unable to create user"
        }

    return {"token": token}


@auth.post("/logout")
def logout_route(authorization: str = Header()):
    user_collection = UserCollection() 

    if not user_collection.get_user(authorization):
        return {"message":"unauthorised access"}

    user_collection.remove_token(authorization)

    return {
        "message" : "Logout successful"
    }

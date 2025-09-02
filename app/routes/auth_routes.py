from fastapi import APIRouter, Response ,Cookie
from app.models.auth_model import Login, Signup, Logout
from app.collections.user_collection import UserCollection
from app.models.db_model import User
from app.common.token_genarator import generate_token
from enum import Enum
from datetime import datetime

class UserType(Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"

auth = APIRouter(
    prefix="/api",
)

@auth.post("/refresh")
def access_token_route(response : Response,refresh_token: str | None = Cookie(default=None)):
    user_collection = UserCollection()

    new_refresh_token = generate_token(128)

    if(not user_collection.update_refresh_token(old_refresh_token=refresh_token,new_refresh_token=new_refresh_token)):
        return {"message" : "token not found"}
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/api/refresh"
    )

    user_collection.close_connection()

    return {"message" : "Token updated successfully"}

@auth.post("/refresh/access")
def access_token_route(refresh_token: str | None = Cookie()):

    user_collection = UserCollection()
    
    new_access_token = generate_token(128)

    if(not user_collection.update_access_token(refresh_token,new_access_token)):
        return {"message" : "db error"}

    user_collection.close_connection()

    return {
        "access_token" : new_access_token 
    }

@auth.post("/login")
def login_route(request : Login, response : Response,):

    user_collection = UserCollection()

    user = user_collection.find_user(request.email)

    if not user:
        return {"message": "email error"}
    
    if  user['password'] != request.password :
        return {"message": "password error"}
    
    refresh_token = generate_token(128)
    access_token = generate_token(128)

    if not user_collection.update_tokens_by_email(request.email,refresh_token,access_token):
        return {"message" : "Unable to login"}
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/api/refresh"
    )

    access_token = generate_token(128)

    user_collection.close_connection()
    
    return {"access_token": access_token}
    

@auth.post("/signup")
def signup_route(request : Signup,response : Response):

    user_collection = UserCollection()

    if user_collection.find_user(request.email):
        return {"message": "email is already used"}
    
    refresh_token = generate_token(128)
    access_token = generate_token(128)

    new_user = User(
        name=request.name,
        email=request.email,
        password=request.password,
        type=UserType.USER.value,
        access_token=access_token,
        refresh_token=refresh_token,
        created_at=datetime.now()
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/api/refresh"
    )
    
    if(not user_collection.create_user(new_user)):
        return {
            "message" : "Unable to create user | db error"
        }
    
    user_collection.close_connection()

    return {"access_token": access_token}


@auth.post("/refresh/logout")
def logout_route(response : Response,refresh_token: str | None = Cookie(default=None)):

    user_collection = UserCollection() 

    if not user_collection.check_refresh_token(refresh_token):
        return {"message" : "Can't Logout"}

    if not user_collection.remove_all_tokens(refresh_token):
        return {"message":"unauthorised access"}
    
    response.delete_cookie(key="refresh_token",path="/api/refresh")

    user_collection.close_connection()

    return {
        "message" : "Logout successful"
    }

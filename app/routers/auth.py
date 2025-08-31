from fastapi import APIRouter
from app.models.auth import Login, Signup
from core.db import MongoClient, DBCollections
auth = APIRouter(
    prefix="/api",
)

@auth.post("/login")
def login_route(request : Login):
    return {"message": "Login successful"}
    

@auth.post("/signup")
def signup_route(request : Signup):
    return {"message": "Signup successful"}


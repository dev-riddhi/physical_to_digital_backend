from fastapi import APIRouter,Header
from app.models.user_model import User

guest = APIRouter(
    prefix="/api/guest",
)

@guest.get("/")
def get_token(request : User, authoauthorization: str = Header()):
    return {}


from fastapi import APIRouter, Header

guest = APIRouter(
    prefix="/api/guest",
)


@guest.get("/")
def get_token(authoauthorization: str = Header()):
    return {}

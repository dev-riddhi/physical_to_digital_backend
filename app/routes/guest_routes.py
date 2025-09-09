from fastapi import APIRouter, Header

guest = APIRouter(
    prefix="/api/guest",
)


@guest.post("/create")
def create_guest_route(authoauthorization: str = Header()):
    return {}


@guest.post("/access")
def access_token():
    return {}


@guest.post("/convert")
def convert_image_route():
    return {}

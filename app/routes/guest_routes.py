import datetime
import shutil
from bson import ObjectId
from fastapi import APIRouter, Header, UploadFile, File
from app.collections.guest_collection import GuestCollection
from app.common.token_genarator import generate_token
from app.common.response_structure import custom_response, error_response
from app.models.db_model import Guest, History, Image
from app.collections.history_collection import HistoryCollection
from app.collections.image_collection import ImageCollections
from app.common.file_name_genarator import generate_filename

guest = APIRouter(
    prefix="/api/guest",
)


@guest.post("/create")
def create_guest_route():

    guest_collection = GuestCollection()

    access_token = generate_token(128)

    if not guest_collection.create_guest(Guest(limit=5, access_token=access_token)):
        return error_response(message="Unable to create guest")

    return custom_response(
        message="User created",
        code=98765,
        data={"access_token": access_token, "user_type": "guest"},
    )


@guest.post("/access")
def access_token_route(access_token: str | None = Header(default=None)):
    guest_collection = GuestCollection()

    new_access_token = generate_token(128)

    if not guest_collection.read_guest(access_token):
        return error_response(message="Guest does not exsists", code=98765)

    if not guest_collection.update_guest_token(
        access_token=access_token, new_access_token=new_access_token
    ):
        return error_response(message="Guest does not exsists", code=76543)

    return custom_response(
        message="User created",
        code=98765,
        data={"access_token": new_access_token, "user_type": "guest"},
    )


@guest.post("/convert")
def convert_image_route(access_token: str = Header(), files: list[UploadFile] = File()):
    guest_collection = GuestCollection()

    guest = guest_collection.read_guest(access_token=access_token)

    if not guest:
        return error_response(message="Unauthorised access")

    for file in files:

        file_type = file.content_type.split("/")
        if (
            file_type[0] == "image"
            and file_type[1] != "jpeg"
            or "png"
            or "jpg"
            or "webp"
        ):
            return error_response(message="Wrong file type")

    images_ids: list[ObjectId] = []

    for file in files:

        file_type = file.content_type.split("/")

        file_location_name = f"uploads/{generate_filename()}.{file_type[1]}"

        try:
            image_collections = ImageCollections()

            with open(file_location_name, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            image = image_collections.insert_image(
                Image(
                    user_id=ObjectId(guest["_id"]),
                    image_path=file_location_name,
                    uploaded_at=datetime.datetime.now(),
                )
            )

            images_ids.append(image["_id"])

        except:
            return error_response(message="Internal error unable to upload image")

        history_collection = HistoryCollection()

        history = history_collection.create_history(
            History(
                title="euest", creation_data=datetime.datetime.now(), images=images_ids
            )
        )

        if not history:
            return error_response(message="Unexpected error", code=9765432)

    return custom_response(message="success", code=86543, data={})

import datetime
from bson import ObjectId
from fastapi import APIRouter, Header, UploadFile, File, Body
from app.collections.guest_collection import GuestCollection
from app.common.token_genarator import generate_token
from app.common.response_structure import custom_response, error_response
from app.models.db_model import Guest, History, Image
from app.collections.history_collection import HistoryCollection
from app.collections.image_collection import ImageCollections
from app.common.file_name_genarator import generate_filename
from app.common.file_upload import upload_file
from app.common.ocr_model import OcrModel

guest = APIRouter(
    prefix="/api/guest",
)

UPLOAD_DIR = "./app/uploads"


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
def convert_image_route(
    access_token: str = Header(),
    files: list[UploadFile] = File(),
    model: str = Body(),
    title: str = Body(),
):
    guest_collection = GuestCollection()

    guest = guest_collection.read_guest(access_token=access_token)

    if not guest:
        return error_response(message="Unauthorised access")

    for file in files:

        file_type = file.content_type.split("/")

        if file_type[0] != "image":
            return error_response(
                message="Try to upload image type file like 'jpeg' , 'png' , 'jpg'",
                code=9876,
            )
        valid_image_types = ["jpeg", "jpg", "png"]

        if not file_type[1] in valid_image_types:
            return error_response(message="Wrong file type", code=9876543)

    image_paths: list[str] = []

    for file in files:
        image_collections = ImageCollections()

        file_type = file.content_type.split("/")

        file_name = f"{generate_filename()}.{file_type[1]}"

        file_path = upload_file("guest", file_name, file.file)

        if not file_path:
            return error_response(
                message="Internal error unable to upload image", code=9876543
            )

        image = Image(
            user_id=ObjectId(guest["_id"]),
            image_path=file_path,
            user_type="guest",
            uploaded_at=datetime.datetime.now(),
        )

        if not image_collections.insert_image(image):
            return error_response(message="Unable to upload", code=987654)

        image_paths.append(file_path)

    response_text_list: list[str] = []

    ocr_model = OcrModel()
    text: str = ""

    for path in image_paths:
        text = ""
        if model == "paddle":
            text = ocr_model.paddle_ocr(path)
        else:
            text = ocr_model.tesseract_ocr(path)

        response_text_list.append(text)

    if not guest_collection.update_limit(
        access_token, guest["limit"] - 1 if guest["limit"] > 0 else 0
    ):
        return error_response(message="limit reached", code=987654)

    return custom_response(
        message="success", code=86543, data={"text": response_text_list}
    )

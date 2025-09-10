from fastapi import APIRouter, Header, File, UploadFile, Response, Body
from datetime import datetime
from app.models.db_model import Image, History
from app.collections.history_collection import HistoryCollection
from app.common.file_upload import upload_file
from app.collections.user_collection import UserCollection
from app.collections.image_collection import ImageCollections
from app.models.request_model import UpdateUser, DeleteUser
from app.common.ocr_model import OcrModel
from app.common.response_structure import (
    error_response,
    custom_response,
    success_response,
)
from app.common.file_name_genarator import generate_filename

user = APIRouter(prefix="/api/user")


@user.get("/")
def get_user_route(access_token=Header()):
    user_collection = UserCollection()

    user = user_collection.read_user(access_token)

    if not user:
        return error_response(code=401, message="User not found")

    if user["type"] != "user":
        return error_response(code=402, message="Unauthorised Access")

    return custom_response(
        code=71343,
        message="Data fetched successfully",
        data={"name": user["name"], "email": user["email"], "history": user["history"]},
    )


@user.put("/update")
def update_user_route(user_data: UpdateUser, access_token=Header()):
    user_collection = UserCollection()

    user = user_collection.read_user(access_token)

    if not user:
        return error_response(message="User not found", code=2348765)

    if user_data.name.strip() == "":
        return error_response(message="Name is empty", code=98765)

    user["name"] = user_data.name

    if user_data.email.strip() == "":
        return error_response(message="Email is empty", code=98709876543265)

    if not user_collection.find_user(user_data.email):
        return error_response(message="Email already in use", code=98765)

    user["email"] = user_data.email

    if not (
        user["password"] == user_data.old_password
        and user_data.new_password.strip() != ""
    ):
        return error_response(message="Wrong password or empty password", code=87654)

    user["password"] = user_data.new_password

    if not user_collection.update_user(access_token=access_token, update_data=user):
        return error_response(message="Unable to change details", code=76543)

    return success_response(message="Details Changed Successfully", code=48752890189)


@user.delete("/delete")
def delete_user_route(user_data: DeleteUser, access_token=Header()):

    if user_data.password.strip() == "":
        return error_response(message="Wrong Password", code=10000000)

    user_collection = UserCollection()

    user = user_collection.read_user(access_token=access_token)

    if not user:
        return error_response(message="User not found", code=90843265)

    if not user_collection.delete_user(
        access_token=access_token, password=user_data.password
    ):
        return error_response(message="Unauthorised access")

    return success_response(message="Account Deleted Successfully", code=32456332890)


@user.post("/convert")
def convert_images(
    model: str = Body(),
    title: str = Body(),
    files: list[UploadFile] = File(),
    access_token=Header(),
):

    user_collection = UserCollection()

    user = user_collection.read_user(access_token=access_token)

    if not user:
        return error_response(message="User not found", code=987654)

    if user["type"] != "user":
        return error_response(message="Unauthorised access", code=876543)

    accepted_file_types = ["jpeg", "png", "jpg", "webp"]

    for file in files:
        file_type = file.content_type.split("/")
        if file_type[0] != "image" and file_type[1] not in accepted_file_types:
            return error_response(message="Wrong file type", code=987654)

    image_ids: list[str] = []
    converted_text: list[str] = []
    temp_text: str = ""

    for file in files:

        temp_text = ""

        file_type = file.content_type.split("/")

        file_name = f"{generate_filename()}.{file_type[1]}"

        file_path = upload_file(user_type="user", file_name=file_name, file=file.file)

        if not file_path:
            return error_response(message="Unable to upload file")

        image_collections = ImageCollections()

        image = image_collections.insert_image(
            Image(
                user_id=user["_id"],
                image_path=file_path,
                uploaded_at=datetime.now(),
                user_type="user",
            )
        )

        image_ids.append(image.inserted_id)

        ocr_model = OcrModel()

        if model == "paddle":
            temp_text = ocr_model.paddle_ocr(file_path)
        else:
            temp_text = ocr_model.tesseract_ocr(file_path)

        converted_text.append(temp_text)

    history_collection = HistoryCollection()

    history = History(
        user_id=user["_id"],
        title=title,
        converted_text_list=converted_text,
        creation_date=datetime.now(),
        images=image_ids,
    )

    user_history: list[str] = user["history"]

    new_history = history_collection.create_history(history)

    if not new_history:
        return error_response(message="Internal error", code=87654)

    user_history.append(new_history.inserted_id)

    user_collection.update_history(access_token, user_history)

    return custom_response(message="Success", code=8765, data={"text": converted_text})

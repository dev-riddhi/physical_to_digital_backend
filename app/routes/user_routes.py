from fastapi import APIRouter, Header, File, UploadFile, Response
import shutil
from datetime import datetime
from bson.objectid import ObjectId
from app.models.db_model import Image
from app.collections.history_collection import HistoryCollection
from app.collections.user_collection import UserCollection
from app.collections.image_collection import ImageCollections
from app.models.user_model import UpdateUser, DeleteUser
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

    if user["name"] != user_data.name and user_data.name.strip() != "":
        user["name"] = user_data.name
    if user["email"] != user_data.email and user_data.email.strip() != "":
        user["email"] = user_data.email
    if (
        user["password"] == user_data.old_password
        and user["password"] != user_data.new_password
        and user_data.new_password.strip() != ""
    ):
        user["password"] = user_data.new_password

    user_collection.update_user(access_token=access_token, update_data=user)

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
    response: Response, files: list[UploadFile] = File(), access_token=Header()
):

    user_collection = UserCollection()

    user = user_collection.read_user(access_token=access_token)

    if not user:
        return error_response(message="User not found", code=987654)

    if user["type"] != "user":
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

    for file in files:

        file_type = file.content_type.split("/")

        file_location_name = f"uploads/{generate_filename()}.{file_type[1]}"

        try:
            image_collections = ImageCollections()

            with open(file_location_name, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            image_collections.insert_image(
                Image(
                    user_id=ObjectId(user["_id"]),
                    image_path=file_location_name,
                    uploaded_at=datetime.now(),
                )
            )

            HistoryCollection()

        except:
            return error_response(message="Internal error unable to upload image")

    return success_response(message="")

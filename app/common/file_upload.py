from os import path
import shutil
from typing import BinaryIO


def upload_file(user_type: str, file_name: str, file: BinaryIO) -> str | None:
    UPLOAD_DIR = "./uploads"

    user_type_folder = "/guest"

    if not path.exists(UPLOAD_DIR):
        return None

    if user_type == "user":
        user_type_folder = "/user"

    file_path = path.join(UPLOAD_DIR + user_type_folder, file_name)

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)

        return file_path

    except:
        return None

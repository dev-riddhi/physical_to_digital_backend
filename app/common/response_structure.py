def success_response(message: str, code: int, access_token=None):
    response = {"code": code, "message": message}
    if access_token != None:
        response["access_token"] = access_token
    return response


def error_response(message: str, code: int):
    return {
        "code": code,
        "message": message,
    }


def custom_response(message: str, code: int, data: dict):
    return {"code": code, "message": message, "data": data}

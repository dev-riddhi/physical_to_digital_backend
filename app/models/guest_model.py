from pydantic import BaseModel


class ConvertRequest(BaseModel):
    model: str

from pydantic import BaseModel


class FileCreate(BaseModel):
    filename: str
    size: int
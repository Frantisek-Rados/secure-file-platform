from pydantic import BaseModel
from datetime import datetime


class FileBase(BaseModel):
    filename: str


class FileOut(FileBase):
    id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import datetime


class FileBase(BaseModel):
    filename: str


class FileOut(FileBase):
    id: int
    filepath: str
    owner_id: int
    public_id: str | None = None
    is_public: int
    created_at: datetime

    class Config:
        from_attributes = True
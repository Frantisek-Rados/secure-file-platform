from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
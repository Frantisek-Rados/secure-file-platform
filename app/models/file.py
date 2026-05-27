from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class File(Column):
    pass


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    original_name = Column(String)
    stored_name = Column(String)

    size = Column(Integer)

    owner_email = Column(String)

    sha256 = Column(String, unique=True)

    created_at = Column(DateTime)
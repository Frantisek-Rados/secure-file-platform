from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.core.database import Base


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    # NEW: sharing support
    public_id = Column(String, unique=True, index=True, nullable=True)
    is_public = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
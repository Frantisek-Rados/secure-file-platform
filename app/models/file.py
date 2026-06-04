from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.core.database import Base

class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    filepath = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String)
    stored_name = Column(String)
    size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_email = Column(String, index=True)
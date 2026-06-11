# Import všetkých modelov, aby SQLAlchemy/Alembic videl metadata

from app.models.user import User
from app.models.file import File

__all__ = ["User", "File"]
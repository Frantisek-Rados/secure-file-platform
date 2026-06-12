from fastapi import APIRouter, UploadFile, File as FastAPIFile, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from pathlib import Path
import uuid
import shutil

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings

from app.models.file import File as FileModel
from app.models.user import User
from app.schemas.file import FileOut

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()


@router.post("/upload", response_model=FileOut)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = FileModel(
        filename=file.filename,
        filepath=str(file_path),
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file


@router.get("/files", response_model=list[FileOut])
def get_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(FileModel).filter(FileModel.owner_id == current_user.id).all()


@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # 🔥 TU JE HLAVNÝ FIX — používaš DB PATH, NIE nové skladanie
    file_path = Path(file.filepath)

    if not file_path.is_absolute():
        file_path = Path("/app") / file_path

    file_path = file_path.resolve()

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Physical file not found")

    return FileResponse(
        path=str(file_path),
        filename=file.filename,
        media_type="application/octet-stream"
    )

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"email": user.email}
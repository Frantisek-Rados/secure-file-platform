from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.file import FileRecord

import uuid
import shutil

from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    unique_name = f"{uuid.uuid4()}_{file.filename}"

    file_path = UPLOAD_DIR / unique_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = FileRecord(
        filename=file.filename,
        filepath=str(file_path),
        owner_id=2
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "id": new_file.id,
        "filename": new_file.filename,
        "filepath": new_file.filepath
    }


@router.get("/files")
def get_files(
    db: Session = Depends(get_db)
):
    files = db.query(FileRecord).all()

    return files


@router.get("/files/{file_id}")
def get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    file = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id)
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return file


@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    file = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id)
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if not Path(file.filepath).exists():
        raise HTTPException(
            status_code=404,
            detail="Physical file not found"
        )

    return FileResponse(
        path=file.filepath,
        filename=file.filename,
        media_type="application/octet-stream"
    )
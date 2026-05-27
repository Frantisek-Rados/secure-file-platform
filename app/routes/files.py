from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.file import File as FileModel
from app.core.security import get_current_user
from datetime import datetime
import hashlib
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = [
    ".txt",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg"
]

MAX_FILE_SIZE = 5 * 1024 * 1024


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    # SHA256 HASH
    sha256_hash = hashlib.sha256(
        contents
    ).hexdigest()

    # duplicate check
    existing_file = db.query(FileModel).filter(
        FileModel.sha256 == sha256_hash
    ).first()

    if existing_file:
        raise HTTPException(
            status_code=400,
            detail="Duplicate file detected"
        )

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    db_file = FileModel(
        original_name=file.filename,
        stored_name=unique_filename,
        size=len(contents),
        owner_email=current_user,
        sha256=sha256_hash,
        created_at=datetime.utcnow()
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return {
        "message": "File uploaded successfully",
        "file_id": db_file.id,
        "sha256": sha256_hash
    }


@router.get("/my-files")
def get_my_files(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    files = db.query(FileModel).filter(
        FileModel.owner_email == current_user
    ).all()

    return files


@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_email == current_user
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.stored_name
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Physical file missing"
        )

    return FileResponse(
        path=file_path,
        filename=file.original_name,
        media_type="application/octet-stream"
    )


@router.delete("/delete/{file_id}")
def delete_file(
    file_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_email == current_user
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.stored_name
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(file)
    db.commit()

    return {
        "message": "File deleted successfully"
    }
from fastapi import APIRouter, UploadFile, File as FastAPIFile, Depends, HTTPException
from pathlib import Path
import shutil
import uuid
from datetime import datetime
import os

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.file import File as FileModel
from app.core.database import SessionLocal
from app.core.security import get_current_user
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/upload")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: str = Depends(get_current_user)
):

    allowed_extensions = [".txt", ".pdf", ".png"]

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    await file.seek(0)

    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = SessionLocal()

    db_file = FileModel(
        original_name=file.filename,
        stored_name=unique_filename,
        size=len(contents),
        created_at=datetime.utcnow(),
        owner_email=current_user
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    db.close()

    return {
        "message": "File uploaded successfully",
        "uploaded_by": current_user
    }

@router.get("/my-files")
def get_my_files(
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    files = db.query(FileModel).filter(
    FileModel.owner_email == current_user
    ).all()

    db.close()

    return files
    
    
    # DATABASE
    db = SessionLocal()

    db_file = FileModel(
        original_name=file.filename,
        stored_name=unique_filename,
        size=len(contents),
        created_at=datetime.utcnow(),
        owner_email=current_user
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    db.close()

    return {
        "message": "File uploaded successfully",
        "file_id": db_file.id,
        "stored_as": unique_filename,
        "uploaded_by": current_user
    }


@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    file = db.query(FileModel).filter(
        FileModel.id == file_id
    ).first()

    if not file:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if file.owner_email != current_user:

        db.close()

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    file_path = UPLOAD_DIR / file.stored_name

    db.close()

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

    file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if file.owner_email != current_user:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    file_path = f"uploads/{file.stored_name}"

    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(file)
    db.commit()

    return {
        "message": "File deleted successfully"
    }
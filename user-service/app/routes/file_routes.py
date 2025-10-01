from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid
import hashlib

from app.core.database import get_db
from app.models.storage import StorageFileORM, StorageBackendORM
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.storage_utils import upload_file_to_s3, compute_human_file_size


router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload", response_model=dict)
async def upload_image(
    file: UploadFile,
    backend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    backend = (
        db.query(StorageBackendORM).filter(StorageBackendORM.id == backend_id).first()
    )
    if not backend:
        raise HTTPException(status_code=404, detail="Storage backend not found")

    file_content = await file.read()
    file_size = len(file_content)

    checksum = hashlib.sha256(file_content).hexdigest()

    ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{ext}"

    public_url = await upload_file_to_s3(file, file_name, backend)

    storage_file = StorageFileORM(
        name=file.filename,
        relative_path=file_name,
        mimetype=file.content_type,
        extension=ext,
        file_size=file_size,
        checksum=checksum,
        public_url=public_url,
        backend_id=backend.id,
        created_at=datetime.now(timezone.utc),
    )
    compute_human_file_size(storage_file)
    db.add(storage_file)
    db.commit()
    db.refresh(storage_file)

    return {"id": storage_file.id, "public_url": storage_file.public_url}


@router.get("/{file_id}", response_model=dict)
def get_image(file_id: int, db: Session = Depends(get_db)):
    storage_file = db.query(StorageFileORM).filter(StorageFileORM.id == file_id).first()
    if not storage_file:
        raise HTTPException(status_code=404, detail="File not found")
    return {
        "id": storage_file.id,
        "name": storage_file.name,
        "public_url": storage_file.public_url,
    }

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import shutil
import os

from app.schemas import FileAddSchema, FileSchema
from app.repository.files import add_file, get_file_by_id
from app.core.database import get_async_session

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=FileSchema)
async def upload_csv_file(
    file: UploadFile = File(...),
    name: str = Form(None),
    description: str = Form(None),
    owner_id: UUID = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # 📁 Створення директорії для користувача
    user_dir = os.path.join(UPLOAD_DIR, f"user_{owner_id}")
    os.makedirs(user_dir, exist_ok=True)

    # 🗂️ Збереження файлу
    file_path = os.path.join(user_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🧾 Створення запису в БД
    file_data = FileAddSchema(
    original_filename=name or file.filename,
    description=description
    )
    db_file = await add_file(session, file_data, owner_id=owner_id, path=file_path)
    return db_file


@router.get("/{file_id}", response_model=FileSchema)
async def get_file(file_id: UUID, session: AsyncSession = Depends(get_async_session)):
    file = await get_file_by_id(session, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
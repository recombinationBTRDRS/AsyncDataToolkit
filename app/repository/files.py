from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import DataFile
from app.schemas import FileAddSchema

async def add_file(
    session: AsyncSession,
    file_data: FileAddSchema,
    owner_id: UUID,
    path: str
) -> DataFile:
    data = file_data.model_dump()
    new_file = DataFile(
        **data,
        user_id=owner_id,
        path=path,
    )
    session.add(new_file)
    await session.commit()
    return new_file

async def get_file_by_id(session: AsyncSession, file_id: UUID) -> DataFile | None:
    result = await session.execute(select(DataFile).where(DataFile.id == file_id))
    return result.scalar_one_or_none()
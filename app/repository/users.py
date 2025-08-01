from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import UserOrm
from app.schemas import UserAddSchema

async def add_user(session: AsyncSession, user_data: UserAddSchema) -> UserOrm:
    user = UserOrm(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return user

async def get_user_by_id(session: AsyncSession, user_id: UUID) -> UserOrm | None:
    result = await session.execute(select(UserOrm).where(UserOrm.id == user_id))
    return result.scalar_one_or_none()
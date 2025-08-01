from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas import UserAddSchema, UserSchema, UserIdResponse
from app.repository.users import add_user, get_user_by_id
from app.core.database import get_async_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserIdResponse)
async def create_user(user_data: UserAddSchema, session: AsyncSession = Depends(get_async_session)):
    user = await add_user(session, user_data)
    return UserIdResponse(id=user.id)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
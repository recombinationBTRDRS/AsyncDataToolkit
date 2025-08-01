from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import TaskOrm
from app.schemas import TaskAddSchema

async def add_task(session: AsyncSession, task_data: TaskAddSchema) -> TaskOrm:
    task = TaskOrm(**task_data.model_dump())
    session.add(task)
    await session.commit()
    return task

async def get_task_by_id(session: AsyncSession, task_id: UUID) -> TaskOrm | None:
    result = await session.execute(select(TaskOrm).where(TaskOrm.id == task_id))
    return result.scalar_one_or_none()

async def get_tasks_by_user(session: AsyncSession, user_id: UUID) -> list[TaskOrm]:
    result = await session.execute(select(TaskOrm).where(TaskOrm.user_id == user_id))
    return result.scalars().all()

async def get_tasks_by_file(session: AsyncSession, file_id: UUID) -> list[TaskOrm]:
    result = await session.execute(select(TaskOrm).where(TaskOrm.data_file_id == file_id))
    return result.scalars().all()

async def get_all_tasks(session: AsyncSession) -> list[TaskOrm]:
    result = await session.execute(select(TaskOrm))
    return result.scalars().all()
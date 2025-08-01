from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas import TaskAddSchema, TaskSchema
from app.repository.tasks import (
    add_task,
    get_task_by_id,
    get_tasks_by_user,
    get_tasks_by_file,
    get_all_tasks,
)
from app.core.database import get_async_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskSchema)
async def create_task(task_data: TaskAddSchema, session: AsyncSession = Depends(get_async_session)):
    task = await add_task(session, task_data)
    return task


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(task_id: UUID, session: AsyncSession = Depends(get_async_session)):
    task = await get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/user/{user_id}", response_model=list[TaskSchema])
async def get_tasks_for_user(user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await get_tasks_by_user(session, user_id)


@router.get("/file/{file_id}", response_model=list[TaskSchema])
async def get_tasks_for_file(file_id: UUID, session: AsyncSession = Depends(get_async_session)):
    return await get_tasks_by_file(session, file_id)


@router.get("/", response_model=list[TaskSchema])
async def get_all(session: AsyncSession = Depends(get_async_session)):
    return await get_all_tasks(session)
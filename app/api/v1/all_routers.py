from fastapi import APIRouter
from app.api.v1.users.router import router as users_router
from app.api.v1.files.router import router as files_router
from app.api.v1.tasks.router import router as tasks_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(files_router, prefix="/files", tags=["Files"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
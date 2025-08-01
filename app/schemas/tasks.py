from uuid import UUID
from pydantic import BaseModel, ConfigDict
from ..enums import TaskStatus

class TaskAddSchema(BaseModel):
    command: str
    status: TaskStatus
    user_id: UUID
    data_file_id: UUID

class TaskSchema(TaskAddSchema):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
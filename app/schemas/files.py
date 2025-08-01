from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict
from ..enums import TableStatus

class FileAddSchema(BaseModel):
    original_filename: str 
    description: Optional[str]

class FileSchema(FileAddSchema):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    status: TableStatus
    path: str
    model_config = ConfigDict(from_attributes=True)
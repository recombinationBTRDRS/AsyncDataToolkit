from uuid import UUID
from pydantic import BaseModel, ConfigDict
from ..enums import UserRole

class UserAddSchema(BaseModel):
    name: str
    role: UserRole

class UserSchema(UserAddSchema):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class UserIdResponse(BaseModel):
    id: UUID
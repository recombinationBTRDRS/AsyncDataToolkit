from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Union, Optional
from models import UserRole,TableStatus
from datetime import datetime

class UserAddSchema(BaseModel):
    name : str
    role : UserRole


class UserSchema(UserAddSchema):
    id:int
    model_config = ConfigDict(from_attributes=True)
    
class UserId(BaseModel):
    ok: bool = True
    id:int

class TableAddSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]

class TableSchema(TableAddSchema):
    id : int
    ownet_id : int
    created_at : datetime
    updated_at : datetime
    status : TableStatus
    columns_count : int
    rows_count : int


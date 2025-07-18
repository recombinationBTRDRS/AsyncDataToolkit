from fastapi import APIRouter, Depends
from typing import Annotated
from schemas import UserAddSchema,UserSchema, UserId
from repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/")
async def add_user(user: Annotated[UserAddSchema, Depends()]) -> UserId :
    user_id = await UserRepository.add_one(user)    
    return {"id":user_id}


@router.get("/")
async def get_users() -> list[UserSchema]:
    users= await UserRepository.find_all()
    return users

# router_file = APIRouter(
#     prefix="/files",
#     tags=["files"]
# )


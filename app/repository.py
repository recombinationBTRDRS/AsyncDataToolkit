from database import new_session
from schemas import UserAddSchema, UserSchema, UserId
from models import UserOrm
from sqlalchemy import select


class UserRepository:
    @classmethod
    async def add_one(cls, user:UserAddSchema):
        async with new_session() as session:
            data = user.model_dump()
            new_user = UserOrm(**data)
            session.add(new_user)
            await session.flush()
            await session.commit()            
            return new_user.id


    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_schema = [UserSchema.model_validate(user_model) for user_model in user_models]
            return user_schema
        

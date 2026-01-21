# mypy: disable-error-code=assignment
import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.models import User
from src.app.auth.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, user_in: UserCreate) -> User:
        user = User(email=user_in.email, hashed_password=user_in.password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        if user_in.email:
            user.email = user_in.email
        # if user_in.password: # Password hashing should be handled in service layer
        #     user.hashed_password = user_in.password
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.get_user_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

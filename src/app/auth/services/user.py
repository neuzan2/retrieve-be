import uuid
from typing import List, Optional

from src.app.auth.models import User
from src.app.auth.repositories import UserRepository
from src.app.auth.schemas import UserCreate, UserUpdate
from src.core.security.hashing import Hasher


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.user_repo.get_all_users(skip=skip, limit=limit)

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return await self.user_repo.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repo.get_user_by_email(email)

    async def create_user(self, user_in: UserCreate) -> User:
        hashed_password = Hasher.get_password_hash(user_in.password)
        user_in.password = (
            hashed_password  # Update the password in user_in before passing to repo
        )
        return await self.user_repo.create_user(user_in)

    async def update_user(
            self, user_id: uuid.UUID, user_in: UserUpdate
    ) -> Optional[User]:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            return None
        # if user_in.password: # Password hashing should be handled here if password is part of update
        #     user_in.password = Hasher.get_password_hash(user_in.password)
        return await self.user_repo.update_user(user, user_in)

    async def delete_user(self, user_id: uuid.UUID) -> bool:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            return False
        await self.user_repo.delete_user(user_id)
        return True

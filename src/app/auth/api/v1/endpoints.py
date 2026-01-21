from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.repositories import UserRepository
from src.app.auth.schemas import User as UserSchema, UserCreate
from src.app.auth.services import UserService
from src.db.session import get_db

router = APIRouter()


@router.post("/users/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_create: UserCreate,
        db: AsyncSession = Depends(get_db),
) -> UserSchema:
    user_service = UserService(UserRepository(db))
    user = await user_service.create_user(user_create)
    return user

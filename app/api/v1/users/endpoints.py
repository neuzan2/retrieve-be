import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user import UserService


router = APIRouter()


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.post(
    "/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, tags=["users"]
)
async def create_user(
    user_in: UserCreate, user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user.
    """
    db_user = await user_service.get_user_by_email(user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return await user_service.create_user(user_in)


@router.get("/", response_model=List[UserSchema], tags=["users"])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
):
    """
    Retrieve all users.
    """
    return await user_service.get_all_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserSchema, tags=["users"])
async def read_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)
):
    """
    Retrieve a single user by ID.
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema, tags=["users"])
async def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Update an existing user.
    """
    user = await user_service.update_user(user_id, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)
):
    """
    Delete a user.
    """
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return None

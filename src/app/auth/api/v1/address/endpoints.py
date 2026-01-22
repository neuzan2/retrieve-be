from fastapi import APIRouter, status

from src.app.auth.schemas import User as UserSchema, UserCreate

router = APIRouter(
    prefix="/address",
    tags=["address"]
)


@router.get("/list/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_create: UserCreate,
):
    return {"id": 1, "username": user_create.username, "email": user_create.email}  # Placeholder implementation

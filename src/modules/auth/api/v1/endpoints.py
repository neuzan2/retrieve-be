"""
Authentication API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db import get_db
from src.modules.auth.models.auth import User
from src.modules.auth.repositories.auth import AuthRepository
from src.modules.auth.schemas.token import Token, TokenRefresh
from src.modules.auth.schemas.user import UserCreate, UserResponse
from src.modules.auth.utils.dependencies import (
    get_current_active_user,
    get_current_user,
    oauth2_scheme,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, username, and password.",
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.!

    - **email**: Valid email address
    - **username**: Unique username (3-100 characters)
    - **password**: Password (8-100 characters, must contain uppercase, lowercase, and digit)
    """
    auth_repository = AuthRepository(db)
    user, error = auth_repository.register_user(user_data)

    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    description="Authenticate user and return JWT tokens.",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login with username/email and password.

    Returns access and refresh tokens.
    """
    auth_repository = AuthRepository(db)
    user = auth_repository.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    return auth_repository.create_tokens(user)


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Get new access and refresh tokens using a valid refresh token.",
)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """
    Refresh tokens using a valid refresh token.
    """
    auth_repository = AuthRepository(db)
    tokens = auth_repository.refresh_access_token(token_data.refresh_token)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return tokens


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Invalidate the current access token.",
)
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Logout by blacklisting the current token.
    """
    auth_repository = AuthRepository(db)
    success = auth_repository.blacklist_token(token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to logout"
        )

    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the currently authenticated user's information.",
)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user's information.
    """
    return current_user


@router.get(
    "/verify",
    summary="Verify token",
    description="Verify if the current token is valid.",
)
async def verify_token_endpoint(current_user: User = Depends(get_current_user)):
    """
    Verify the current token is valid.
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": current_user.username,
    }

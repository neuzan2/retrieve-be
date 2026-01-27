"""
User schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Base schema for user data."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user data."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """
    Schema for user response containing public user data.
    This schema extends UserBase and includes additional fields that are returned
    when retrieving user information from the database.
    Attributes:
        id (int): Unique identifier for the user.
        is_active (bool): Flag indicating whether the user account is active.
        created_at (datetime): Timestamp when the user account was created.
    Config:
        from_attributes (bool): Enables Pydantic to populate the model from ORM objects
            by reading attributes directly. This allows the schema to work seamlessly
            with SQLAlchemy models or any object with attributes matching the field names,
            instead of requiring dictionary inputs.
    """

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """Schema for user with hashed password (internal use)."""

    hashed_password: str
    is_superuser: bool
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str = Field(..., description="Username or email")
    password: str = Field(..., min_length=1)

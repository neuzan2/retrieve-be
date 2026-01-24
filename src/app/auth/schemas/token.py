"""
Token schemas for JWT authentication.
"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    username: Optional[str] = None
    user_id: Optional[int] = None
    token_type: Optional[str] = None


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str

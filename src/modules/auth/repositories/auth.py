"""
Authentication service for login, token management, and related operations.
"""

from datetime import datetime, timezone
from functools import cached_property
from typing import Optional, Tuple

from sqlalchemy.orm import Query, Session

from src.modules.auth.models.auth import TokenBlacklist, User
from src.modules.auth.repositories.user import UserRepository
from src.modules.auth.schemas.token import Token
from src.modules.auth.schemas.user import UserCreate
from src.modules.auth.utils.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)


class AuthRepository:
    """Repository class for authentication operations."""

    def __init__(self, db: Session):
        """
        Initialize AuthRepository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.user_repository = UserRepository(db)

    @cached_property
    def query(self) -> Query:
        """Get the current database session."""
        return self.db.query(TokenBlacklist)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username/email and password.

        Args:
            username: Username or email
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.user_repository.get_by_username_or_email(username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def create_tokens(self, user: User) -> Token:
        """
        Create access and refresh tokens for a user.

        Args:
            user: User object to create tokens for

        Returns:
            Token object containing access and refresh tokens
        """
        token_data = {
            "sub": user.username,
            "user_id": user.id,
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    def refresh_access_token(self, refresh_token: str) -> Optional[Token]:
        """
        Create new tokens using a refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New Token object if refresh token is valid, None otherwise
        """
        # Check if refresh token is blacklisted
        blacklisted = self.query.filter(TokenBlacklist.token == refresh_token).first()

        if blacklisted:
            return None

        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")

        if payload is None:
            return None

        username = payload.get("sub")

        if not username:
            return None

        # Get user
        user = self.user_repository.get_by_username(username)

        if not user or not user.is_active:
            return None

        # Create new tokens
        return self.create_tokens(user)

    def register_user(
        self, user_data: UserCreate
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Register a new user.

        Args:
            user_data: User registration data

        Returns:
            Tuple of (User, None) if successful, (None, error_message) if failed
        """
        # Check if email already exists
        if self.user_repository.get_by_email(user_data.email):
            return None, "Email already registered"

        # Check if username already exists
        if self.user_repository.get_by_username(user_data.username):
            return None, "Username already taken"

        # Create user
        user = self.user_repository.create(user_data)

        return user, None

    def blacklist_token(self, token: str) -> bool:
        """
        Add a token to the blacklist (logout).

        Args:
            token: Token to blacklist

        Returns:
            True if successful, False otherwise
        """
        try:
            # Verify token to get expiry
            payload = verify_token(token, token_type="access")
            if not payload:
                # Try as refresh token
                payload = verify_token(token, token_type="refresh")

            if not payload:
                return False

            # Get expiry from token
            exp = payload.get("exp")
            expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)

            # Add to blacklist
            blacklisted_token = TokenBlacklist(token=token, expires_at=expires_at)

            self.db.add(blacklisted_token)
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            return False

    def cleanup_expired_tokens(self) -> int:
        """
        Remove expired tokens from the blacklist.

        Returns:
            Number of tokens removed
        """
        result = self.query.filter(
            TokenBlacklist.expires_at < datetime.now(timezone.utc)
        ).delete()

        self.db.commit()

        return result

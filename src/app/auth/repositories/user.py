"""
User service for CRUD operations.
"""

from functools import cached_property
from typing import Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from src.app.auth.models.auth import User
from src.app.auth.schemas.user import UserCreate, UserUpdate
from src.app.auth.utils.security import get_password_hash


class UserRepository:
    """Repository class for user-related operations."""

    def __init__(self, db: AsyncSession):
        """
        Initialize UserRepository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    @cached_property
    def query(self) -> Query:
        """Get the current database session."""
        return Select(User)

    async def get_object(self, filter_by: dict) -> Optional[User]:
        """
        Get a user object based on filter criteria.

        Args:
            filter_by: Dictionary of filter criteria

        Returns:
            User object if found, None otherwise
        """
        result = self.db.execute(self.query.where(**filter_by))
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID to search for

        Returns:
            User object if found, None otherwise
        """
        return await self.get_object(User.id == user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: Email address to search for

        Returns:
            User object if found, None otherwise
        """
        return await self.get_object(User.email == email)

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username to search for

        Returns:
            User object if found, None otherwise
        """
        return self.query.filter(User.username == username).first()

    async def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """
        Get user by username or email.

        Args:
            identifier: Username or email to search for

        Returns:
            User object if found, None otherwise
        """
        result = await self.db.execute(
            self.query.where((User.username == identifier) | (User.email == identifier))
        )
        return result.scalars().first()

    async def create(self, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created User object
        """
        hashed_password = get_password_hash(user_data.password)

        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    async def update(self, user: User, user_data: UserUpdate) -> User:
        """
        Update an existing user.

        Args:
            user: User object to update
            user_data: Update data

        Returns:
            Updated User object
        """
        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    async def delete(self, user: User) -> None:
        """
        Delete a user.

        Args:
            user: User object to delete
        """
        self.db.delete(user)
        self.db.commit()

    async def activate(self, user: User) -> User:
        """
        Activate a user account.

        Args:
            user: User object to activate

        Returns:
            Updated User object
        """
        user.is_active = True
        self.db.commit()
        self.db.refresh(user)
        return user

    async def deactivate(self, user: User) -> User:
        """
        Deactivate a user account.

        Args:
            user: User object to deactivate

        Returns:
            Updated User object
        """
        user.is_active = False
        self.db.commit()
        self.db.refresh(user)
        return user

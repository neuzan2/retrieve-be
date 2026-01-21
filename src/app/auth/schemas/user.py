import uuid
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr


# Properties to receive on user creation
class UserCreate(UserBase):
    password: str


# Properties to receive on user update
class UserUpdate(UserBase):
    pass


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

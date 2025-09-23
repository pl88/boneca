"""User data models and schemas.

This module defines the data models and schemas used for user-related operations.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.domain.users.models import UserPermission


class UserBase(BaseModel):
    """Base fields shared by user schemas."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    permissions: UserPermission = UserPermission.STUDENT


class UserCreate(UserBase):
    """Payload for creating a user."""

    pass


class UserRead(UserBase):
    """Response schema for returning a user."""

    id: int

    class Config:
        """Pydantic configuration for ORM mode and model parsing."""

        from_attributes = True


class UserUpdate(BaseModel):
    """Payload for partially updating a user."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    permissions: Optional[UserPermission] = None

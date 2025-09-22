"""User domain models using SQLModel.

This module defines the SQLModel database models for user-related entities.
"""
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class UserPermission(str, Enum):
    """User permission levels."""
    
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    VIEWER = "viewer"


class User(SQLModel, table=True):
    """User database model.
    
    Represents a user in the Boneca dance school management system.
    
    Attributes:
        id: Primary key identifier
        first_name: User's first name
        last_name: User's last name
        email: User's email address (unique)
        permissions: User's permission level
    """
    
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=100, nullable=False)
    last_name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True, index=True)
    permissions: UserPermission = Field(default=UserPermission.STUDENT)
    
    model_config = {"from_attributes": True}
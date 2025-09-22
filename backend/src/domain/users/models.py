"""User domain models using SQLModel.

This module defines the SQLModel database models for user-related entities.
"""
from enum import Enum
from typing import Optional

from email_validator import EmailNotValidError, validate_email
from pydantic import field_validator
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

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if not v or not v.strip():
            raise ValueError("Email cannot be empty")

        try:
            # Use email-validator directly
            valid_email = validate_email(v)
            return valid_email.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {str(e)}")

    model_config = {"from_attributes": True}

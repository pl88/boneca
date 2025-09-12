"""User data models and schemas.

This module defines the data models and schemas used for user-related operations.
"""
from pydantic import BaseModel


class UserCreate(BaseModel):
    """User creation model.

    Attributes:
        name: The name of the user.
    """

    name: str

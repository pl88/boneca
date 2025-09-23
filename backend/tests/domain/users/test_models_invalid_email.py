"""Invalid email tests for User model validator using Pydantic validation."""
import pytest
from pydantic import ValidationError

from src.domain.users.models import User


class TestUserModelInvalidEmail:
    def test_empty_email_raises(self) -> None:
        with pytest.raises(ValidationError):
            User.model_validate({"first_name": "A", "last_name": "B", "email": ""})

    def test_whitespace_email_raises(self) -> None:
        with pytest.raises(ValidationError):
            User.model_validate({"first_name": "A", "last_name": "B", "email": "   "})

    def test_bad_format_email_raises(self) -> None:
        with pytest.raises(ValidationError):
            User.model_validate({"first_name": "A", "last_name": "B", "email": "not-an-email"})

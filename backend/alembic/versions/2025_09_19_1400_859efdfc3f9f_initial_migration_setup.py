"""Initial migration setup

Revision ID: 859efdfc3f9f
Revises: 
Create Date: 2025-09-19 14:00:11.824399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '859efdfc3f9f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The boneca schema is already created by our database init script
    # This migration serves as the initial tracking point for Alembic
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # For the initial migration, we don't need to do anything
    pass

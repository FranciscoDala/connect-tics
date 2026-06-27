"""add likes dislikes to post_images

Revision ID: 269036675ed3
Revises: 1f5a1edbf806
Create Date: 2026-06-27 19:21:52.642601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '269036675ed3'
down_revision: Union[str, Sequence[str], None] = '1f5a1edbf806'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

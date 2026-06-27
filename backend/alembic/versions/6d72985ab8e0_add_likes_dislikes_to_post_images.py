"""add likes dislikes to post_images

Revision ID: 6d72985ab8e0
Revises: 269036675ed3
Create Date: 2026-06-27 19:22:44.592269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d72985ab8e0'
down_revision: Union[str, Sequence[str], None] = '269036675ed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""teste final

Revision ID: 1f5a1edbf806
Revises: c2611ed89937
Create Date: 2026-06-27 16:27:57.788497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f5a1edbf806'
down_revision: Union[str, Sequence[str], None] = 'c2611ed89937'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

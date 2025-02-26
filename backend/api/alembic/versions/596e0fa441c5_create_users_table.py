"""create_users_table

Revision ID: 596e0fa441c5
Revises: be2d2ef14e27
Create Date: 2025-02-25 16:31:54.428427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '596e0fa441c5'
down_revision: Union[str, None] = 'be2d2ef14e27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 
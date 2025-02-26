"""create_users_table

Revision ID: be2d2ef14e27
Revises: a374293c7c5c
Create Date: 2025-02-25 16:20:53.177746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be2d2ef14e27'
down_revision: Union[str, None] = 'a374293c7c5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 
"""database migration

Revision ID: 18fcc6e93f7f
Revises: e53fbd2b7eaa
Create Date: 2025-02-25 04:07:51.421913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18fcc6e93f7f'
down_revision: Union[str, None] = 'e53fbd2b7eaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 
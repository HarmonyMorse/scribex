"""change_ids_to_uuid

Revision ID: 6ae5136af94e
Revises: 18fcc6e93f7f
Create Date: 2025-02-25 04:19:34.698435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ae5136af94e'
down_revision: Union[str, None] = '18fcc6e93f7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 
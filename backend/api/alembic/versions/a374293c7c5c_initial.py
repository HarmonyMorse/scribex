"""initial

Revision ID: a374293c7c5c
Revises: 34550f47b518
Create Date: 2025-02-25 16:19:07.493276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a374293c7c5c'
down_revision: Union[str, None] = '34550f47b518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 
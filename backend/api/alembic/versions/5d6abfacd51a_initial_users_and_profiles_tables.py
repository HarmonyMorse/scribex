"""Initial users and profiles tables

Revision ID: 5d6abfacd51a
Revises: 
Create Date: 2025-02-25 00:30:27.365423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d6abfacd51a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_type', sa.Enum('STUDENT', 'TEACHER', 'PARENT', 'ADMIN', name='usertype'), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('parent_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade_level', sa.Integer(), nullable=True),
    sa.Column('has_iep', sa.Boolean(), nullable=True),
    sa.Column('iep_summary', sa.String(), nullable=True),
    sa.Column('accommodations', sa.JSON(), nullable=True),
    sa.Column('iep_goals', sa.JSON(), nullable=True),
    sa.Column('last_iep_review', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_area', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parent_student_association',
    sa.Column('parent_profile_id', sa.Integer(), nullable=True),
    sa.Column('student_profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_profile_id'], ['parent_profiles.id'], ),
    sa.ForeignKeyConstraint(['student_profile_id'], ['student_profiles.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parent_student_association')
    op.drop_table('teacher_profiles')
    op.drop_table('student_profiles')
    op.drop_table('parent_profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

parent_student_association = Table(
    'parent_student_association',
    Base.metadata,
    Column('parent_id', UUID(as_uuid=True), ForeignKey('parent_profiles.id')),
    Column('student_id', UUID(as_uuid=True), ForeignKey('student_profiles.id'))
) 
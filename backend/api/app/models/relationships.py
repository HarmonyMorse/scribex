from sqlalchemy import Table, Column, ForeignKey, Integer
from .base import Base

parent_student_association = Table(
    "parent_student_association",
    Base.metadata,
    Column("parent_profile_id", Integer, ForeignKey("parent_profiles.id")),
    Column("student_profile_id", Integer, ForeignKey("student_profiles.id")),
) 
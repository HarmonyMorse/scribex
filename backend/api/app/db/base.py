from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base

# Import all models here so that Base has them before creating tables
from app.models.user import User  # noqa
from app.models.profiles import BaseProfile, StudentProfile, TeacherProfile, ParentProfile  # noqa 
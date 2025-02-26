from .base import Base
from .user import User
from .profiles import BaseProfile, StudentProfile, TeacherProfile, ParentProfile
from .relationships import parent_student_association

# This ensures all models are registered with Base.metadata
__all__ = [
    "Base",
    "User",
    "BaseProfile",
    "StudentProfile",
    "TeacherProfile", 
    "ParentProfile",
    "parent_student_association"
] 
from enum import Enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, Boolean, JSON, DateTime
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .relationships import parent_student_association

class UserType(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"

class BaseProfile(Base):
    __tablename__ = "profiles"
    
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), unique=True)
    user_type: Mapped[UserType] = Column(SQLEnum(UserType))
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    type: Mapped[str] = Column(String(50))
    
    # Relationship with User
    user: Mapped["User"] = relationship("User", back_populates="profile")
    
    __mapper_args__ = {
        "polymorphic_identity": "base",
        "polymorphic_on": "type"
    }

class StudentProfile(BaseProfile):
    __tablename__ = "student_profiles"
    
    id: Mapped[int] = Column(Integer, ForeignKey("profiles.id"), primary_key=True)
    grade_level: Mapped[int] = Column(Integer)
    has_iep: Mapped[bool] = Column(Boolean, default=False)
    # IEP Details
    iep_summary: Mapped[Optional[str]] = Column(String, nullable=True)
    accommodations: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    iep_goals: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    last_iep_review: Mapped[Optional[datetime]] = Column(DateTime, nullable=True)
    
    # Relationships
    parents: Mapped[List["ParentProfile"]] = relationship(
        "ParentProfile",
        secondary=parent_student_association,
        back_populates="students"
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

class TeacherProfile(BaseProfile):
    __tablename__ = "teacher_profiles"
    
    id: Mapped[int] = Column(Integer, ForeignKey("profiles.id"), primary_key=True)
    subject_area: Mapped[str] = Column(String)
    
    __mapper_args__ = {
        "polymorphic_identity": "teacher"
    }

class ParentProfile(BaseProfile):
    __tablename__ = "parent_profiles"
    
    id: Mapped[int] = Column(Integer, ForeignKey("profiles.id"), primary_key=True)
    
    # Relationships
    students: Mapped[List["StudentProfile"]] = relationship(
        "StudentProfile",
        secondary=parent_student_association,
        back_populates="parents"
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "parent"
    } 
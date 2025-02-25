from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from uuid import UUID, uuid4
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = Column(PGUUID, primary_key=True, default=uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type = Column(String)  # "student", "teacher", "guardian"
    
    # Relationship with profile
    profile = relationship("BaseProfile", back_populates="user", uselist=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

class Student(User):
    __tablename__ = "students"
    
    id: Mapped[UUID] = Column(PGUUID, ForeignKey("users.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

class Teacher(User):
    __tablename__ = "teachers"
    
    id: Mapped[UUID] = Column(PGUUID, ForeignKey("users.id"), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

class Guardian(User):
    __tablename__ = "guardians"
    
    id: Mapped[UUID] = Column(PGUUID, ForeignKey("users.id"), primary_key=True)
    student_id: Mapped[UUID] = Column(PGUUID, ForeignKey("students.id"))
    student = relationship("Student", foreign_keys=[student_id])
    
    __mapper_args__ = {
        'polymorphic_identity': 'guardian',
    } 
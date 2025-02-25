from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    hashed_password: Mapped[str] = Column(String)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    profile: Mapped["BaseProfile"] = relationship("BaseProfile", back_populates="user", uselist=False) 
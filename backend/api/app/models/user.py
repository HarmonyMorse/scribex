from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, relationship

from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    hashed_password: Mapped[str] = Column(String)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    profile: Mapped["BaseProfile"] = relationship("BaseProfile", back_populates="user", uselist=False) 
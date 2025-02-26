from sqlalchemy import Column, String, Boolean, DateTime, TypeDecorator
from sqlalchemy.sql import func
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from .base import Base

class UUIDType(TypeDecorator):
    """Platform-independent UUID type.
    Uses String as the base type for SQLite compatibility."""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return UUID(value)

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUIDType, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    profile = relationship("BaseProfile", back_populates="user", uselist=False) 
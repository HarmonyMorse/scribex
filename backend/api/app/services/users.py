from datetime import datetime
from typing import Optional, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import get_password_hash
from app.models import User, StudentProfile, TeacherProfile, ParentProfile
from app.schemas.profiles import StudentCreate, TeacherCreate, GuardianCreate

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_student(self, data: StudentCreate) -> User:
        # Create user
        db_user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True
        )
        self.db.add(db_user)
        
        # Create student profile
        profile = StudentProfile(
            user=db_user,
            **data.profile.dict()
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def create_teacher(self, data: TeacherCreate) -> User:
        db_user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True
        )
        self.db.add(db_user)
        
        profile = TeacherProfile(
            user=db_user,
            **data.profile.dict()
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def create_guardian(self, data: GuardianCreate) -> User:
        db_user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True
        )
        self.db.add(db_user)
            
        profile = ParentProfile(
            user=db_user,
            **data.profile.dict()
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def upsert_user(self, user_id: int, user_data: dict) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Handle profile updates
        if "profile" in user_data:
            profile_data = user_data.pop("profile")
            for key, value in profile_data.items():
                setattr(user.profile, key, value)

        # Handle user updates
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user 
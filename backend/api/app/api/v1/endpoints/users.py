from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.services.users import UserService
from app.schemas.profiles import StudentCreate, TeacherCreate, GuardianCreate
from app.models import User

router = APIRouter()

@router.post("/student",
    response_model=dict,
    summary="Create new student account",
    description="Creates a new student account with associated profile and required fields",
    responses={
        200: {
            "description": "Student account created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "jsmith2024",
                        "email": "john.smith@school.edu",
                        "id": 1
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    user_service = UserService(db)
    try:
        user = user_service.create_student(student)
        return {"username": user.username, "email": user.email, "id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/teacher",
    response_model=dict,
    summary="Create new teacher account",
    description="Creates a new teacher account with associated profile and subject area",
    responses={
        200: {
            "description": "Teacher account created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "ms.jones",
                        "email": "jones@school.edu",
                        "id": 1
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    user_service = UserService(db)
    try:
        user = user_service.create_teacher(teacher)
        return {"username": user.username, "email": user.email, "id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/guardian",
    response_model=dict,
    summary="Create new guardian account",
    description="Creates a new guardian account with optional student associations",
    responses={
        200: {
            "description": "Guardian account created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "username": "parent.smith",
                        "email": "parent@email.com",
                        "id": 1
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_guardian(
    guardian: GuardianCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    user_service = UserService(db)
    try:
        user = user_service.create_guardian(guardian)
        return {"username": user.username, "email": user.email, "id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", 
    response_model=dict,
    summary="Get user profile",
    description="Fetches all relevant user profile information, including roles, accommodations, and associated data"
)
def get_user(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    user_service = UserService(db)
    user = user_service.get_user_with_profile(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/{user_id}",
    response_model=dict,
    summary="Update user profile",
    description="Updates or inserts user profile information (e.g. name, accommodations, contact info)"
)
def update_user(
    user_id: int,
    user_data: dict,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    user_service = UserService(db)
    try:
        user = user_service.upsert_user(user_id, user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}",
    response_model=dict,
    summary="Delete user",
    description="Removes a user from the system and revokes all associated access"
)
def delete_user(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> Any:
    user_service = UserService(db)
    try:
        user_service.delete_user(user_id)
        return {"message": "User successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
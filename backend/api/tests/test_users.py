import pytest
from fastapi.testclient import TestClient
from typing import Dict
from .mocks.user_service import mock_user_service

def test_create_student_success(client: TestClient):
    """Test successful student creation"""
    response = client.post(
        "/api/users/student",
        json={
            "username": "test_student",
            "email": "student@test.com",
            "password": "StrongPass123!",
            "profile": {
                "first_name": "Test",
                "last_name": "Student",
                "grade_level": 6,
                "has_iep": False
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == "test_student"
    assert "password" not in data

def test_create_student_with_iep(client: TestClient):
    """Test student creation with IEP details"""
    response = client.post(
        "/api/users/student",
        json={
            "username": "iep_student",
            "email": "iep.student@test.com",
            "password": "StrongPass123!",
            "profile": {
                "first_name": "IEP",
                "last_name": "Student",
                "grade_level": 7,
                "has_iep": True,
                "iep_summary": "Reading comprehension focus",
                "accommodations": {
                    "extended_time": True,
                    "text_to_speech": True
                }
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["profile"]["has_iep"] == True
    assert "iep_summary" in data["profile"]

def test_create_student_duplicate_username(client: TestClient):
    """Test creating student with duplicate username"""
    # Create first student
    client.post(
        "/api/users/student",
        json={
            "username": "duplicate_user",
            "email": "first@test.com",
            "password": "StrongPass123!",
            "profile": {
                "first_name": "First",
                "last_name": "User",
                "grade_level": 6,
                "has_iep": False
            }
        }
    )
    
    # Try to create second student with same username
    response = client.post(
        "/api/users/student",
        json={
            "username": "duplicate_user",
            "email": "second@test.com",
            "password": "StrongPass123!",
            "profile": {
                "first_name": "Second",
                "last_name": "User",
                "grade_level": 6,
                "has_iep": False
            }
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_create_teacher_success(client: TestClient):
    """Test successful teacher creation"""
    response = client.post(
        "/api/users/teacher",
        json={
            "username": "test_teacher",
            "email": "teacher@test.com",
            "password": "StrongPass123!",
            "profile": {
                "first_name": "Test",
                "last_name": "Teacher",
                "subject_areas": ["Math", "Science"],
                "grade_levels": [6, 7, 8]
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert len(data["profile"]["subject_areas"]) == 2

@pytest.fixture
def test_user(client: TestClient) -> Dict:
    """Fixture to create a test user"""
    response = client.post(
        "/api/users/student",
        json={
            "username": "fixture_user",
            "email": "fixture@test.com",
            "password": "StrongPass123!",
            "profile": {
                "first_name": "Fixture",
                "last_name": "User",
                "grade_level": 6,
                "has_iep": False
            }
        }
    )
    return response.json() 
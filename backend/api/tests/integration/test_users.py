import pytest
from fastapi.testclient import TestClient

@pytest.mark.parametrize("test_data", [
    {
        "username": "test_student1",
        "email": "student1@test.com",
        "password": "testpass123",
        "profile": {
            "first_name": "Test",
            "last_name": "Student",
            "grade_level": 6,
            "has_iep": False
        }
    },
    {
        "username": "test_student2",
        "email": "student2@test.com",
        "password": "testpass123",
        "profile": {
            "first_name": "Test2",
            "last_name": "Student2",
            "grade_level": 7,
            "has_iep": True,
            "iep_summary": "Test IEP",
            "accommodations": {"extra_time": True},
            "iep_goals": {"writing": "Improve paragraph structure"}
        }
    }
])
def test_create_student(client, test_data):
    response = client.post("/api/users/student", json=test_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_data["username"]
    assert "password" not in data

def test_create_teacher(client):
    response = client.post(
        "/api/users/teacher",
        json={
            "username": "test_teacher",
            "email": "teacher@test.com",
            "password": "testpass123",
            "profile": {
                "first_name": "Test",
                "last_name": "Teacher",
                "subject_areas": ["English"],
                "grade_levels": [9, 10, 11]
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_teacher"
    assert "password" not in data

def test_create_guardian(client):
    # First create a student to associate with
    student_response = client.post(
        "/api/users/student",
        json={
            "username": "test_student3",
            "email": "student3@test.com",
            "password": "testpass123",
            "profile": {
                "first_name": "Test",
                "last_name": "Student",
                "grade_level": 8,
                "has_iep": False
            }
        }
    )
    student_id = student_response.json()["id"]
    
    # Then create guardian
    response = client.post(
        "/api/users/guardian",
        json={
            "username": "test_guardian",
            "email": "guardian@test.com",
            "password": "testpass123",
            "profile": {
                "first_name": "Test",
                "last_name": "Guardian",
                "relationship": "Parent",
                "student_ids": [student_id]
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_guardian"
    assert "password" not in data 
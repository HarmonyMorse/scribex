from typing import Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class MockUserService:
    def __init__(self):
        self.users: Dict[UUID, Dict] = {}
        
    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user"""
        user_id = uuid4()
        user = {
            "id": user_id,
            "username": user_data["username"],
            "email": user_data["email"],
            "hashed_password": user_data["hashed_password"],
            "user_type": user_data.get("user_type", "student"),
            "profile": user_data.get("profile", {}),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self.users[user_id] = user
        return user
        
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        for user in self.users.values():
            if user["username"] == username:
                return user
        return None
        
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
        
    def get_user_by_id(self, user_id: UUID) -> Optional[Dict]:
        """Get user by ID"""
        return self.users.get(user_id)
        
    def update_user(self, user_id: UUID, update_data: Dict) -> Optional[Dict]:
        """Update user data"""
        if user_id in self.users:
            self.users[user_id].update(update_data)
            self.users[user_id]["updated_at"] = datetime.utcnow()
            return self.users[user_id]
        return None
        
    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

# Global instance for use in tests
mock_user_service = MockUserService() 
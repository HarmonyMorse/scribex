from typing import Dict, Optional, Union, Set
from uuid import UUID, uuid4
from datetime import datetime
from ..core.security import get_password_hash, verify_password

class MockUserService:
    """Mock user service for testing"""
    def __init__(self):
        self.users: Dict[UUID, Dict] = {}
        self.blacklisted_tokens: Set[str] = set()
        
    def create_user(self, username: str, email: str, password: str, user_type: str, profile: Optional[Dict] = None) -> Dict:
        """Create a new user"""
        user_id = uuid4()
        user = {
            "id": str(user_id),
            "username": username,
            "email": email,
            "hashed_password": get_password_hash(password),
            "user_type": user_type,
            "is_active": True,
            "profile": profile or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self.users[user_id] = user
        return {**user, "hashed_password": None}
    
    def get_user_by_id(self, user_id: Union[UUID, str]) -> Optional[Dict]:
        """Get user by ID"""
        if isinstance(user_id, str):
            try:
                user_id = UUID(user_id)
            except ValueError:
                return None
        
        user = self.users.get(user_id)
        if user:
            return {**user, "id": str(user_id)}
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        for user_id, user in self.users.items():
            if user["username"] == username:
                return {**user, "id": str(user_id)}
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        for user_id, user in self.users.items():
            if user["email"] == email:
                return {**user, "id": str(user_id)}
        return None
    
    def update_user(self, user_id: Union[UUID, str], update_data: Dict) -> Optional[Dict]:
        """Update user data"""
        if isinstance(user_id, str):
            try:
                user_id = UUID(user_id)
            except ValueError:
                return None
        
        if user_id in self.users:
            self.users[user_id].update(update_data)
            self.users[user_id]["updated_at"] = datetime.utcnow()
            return {**self.users[user_id], "hashed_password": None}
        return None
    
    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return verify_password(plain_password, hashed_password)
    
    def blacklist_token(self, token: str) -> None:
        """Add a token to the blacklist"""
        self.blacklisted_tokens.add(token)
    
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted"""
        return token in self.blacklisted_tokens 
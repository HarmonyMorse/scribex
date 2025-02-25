from pydantic import BaseModel

class Token(BaseModel):
    """Token schema for authentication responses"""
    access_token: str
    token_type: str
    refresh_token: str | None = None

class RefreshToken(BaseModel):
    """Schema for refresh token requests"""
    refresh_token: str 
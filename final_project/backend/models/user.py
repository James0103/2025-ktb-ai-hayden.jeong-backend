"""
User Pydantic models for API validation and serialization
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Model for creating a new user"""
    nickname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """Model for login user"""
    email: EmailStr
    password: str = Field(..., min_length=6)

class User(BaseModel):
    """User model for database"""
    id: Optional[int] = None
    nickname: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    profile_photo: Optional[str] = None
    create_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Response model for user information (without sensitive data)"""
    id: int
    nickname: str
    email: EmailStr
    profile_photo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


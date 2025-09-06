from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AuthProvider(str, Enum):
    EMAIL = "email"
    
    # 🏗️ TODO: Add X and Instagram
    X = "x"
    INSTAGRAM = "instagram"

class UserRegisterRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResendOTPRequest(BaseModel):
    email: EmailStr

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    uid: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    provider: AuthProvider
    is_new_user: Optional[bool] = False
    premium: Optional[bool] = False

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse
    expires_in: int

class UserProfile(BaseModel):
    """
    Complete user profile model matching your database schema
    """
    uid: str
    email: str
    premium: bool = False
    created_at: datetime
    language: List[str] = []  # Array of language codes
    age: Optional[int] = None
    gender: Optional[str] = None  # 'male', 'female', 'other', 'prefer_not_to_say'
    x_account: Optional[str] = None
    ig_account: Optional[str] = None

class UserUpdateRequest(BaseModel):
    """
    Model for updating user profile
    """
    display_name: Optional[str] = None
    language: Optional[List[str]] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    x_account: Optional[str] = None
    ig_account: Optional[str] = None

class EmailCheckResponse(BaseModel):
    email: str
    user_exists: bool
    suggested_action: str  # "login" or "register"
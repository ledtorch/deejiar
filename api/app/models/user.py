from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AuthProvider(str, Enum):
    EMAIL = "email"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"

class UserRegisterRequest(BaseModel):
    email: EmailStr
    
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=4)

class ResendOTPRequest(BaseModel):
    email: EmailStr

class UserLoginRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=4)

class UserProfile(BaseModel):
    uid: str
    email: EmailStr
    provider: AuthProvider
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: datetime
    metadata: Optional[Dict[str, Any]] = {}
    
class UserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    provider: AuthProvider
    
class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse
    expires_in: int
    
class TokenRefreshRequest(BaseModel):
    refresh_token: str
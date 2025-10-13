from pydantic import BaseModel, EmailStr, Field
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
    
    # Add missing fields that exist in database
    created_at: Optional[datetime] = None
    language: Optional[List[str]] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
    # Social account fields (using field names that match your database)
    x_account: Optional[str] = Field(None, alias="x-account")
    ig_account: Optional[str] = Field(None, alias="ig-account")
    x_connected: Optional[datetime] = Field(None, alias="x-connected")
    ig_connected: Optional[datetime] = Field(None, alias="ig-connected")

    # Subscription
    premium: Optional[bool] = False
    subscription_plan: Optional[str] = None                 # e.g. "com.deejiar.premium.brass.monthly.v1"
    subscription_status: Optional[str] = None               # "active" | "trial" | "expired" | "cancelled"
    subscription_started_at: Optional[datetime] = None
    subscription_expires_at: Optional[datetime] = None

    class Config:
        # Allow field aliases to work
        allow_population_by_field_name = True

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
    created_at: datetime
    language: List[str] = []  # Array of language codes
    age: Optional[int] = None
    gender: Optional[str] = None  # 'male', 'female', 'other', 'prefer_not_to_say'
    x_account: Optional[str] = None
    ig_account: Optional[str] = None

    # Subscription
    premium: Optional[bool] = False
    subscription_plan: Optional[str] = None
    subscription_status: Optional[str] = None
    subscription_started_at: Optional[datetime] = None
    subscription_expires_at: Optional[datetime] = None

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
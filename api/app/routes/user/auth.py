from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional

from app.models.user import (
    UserRegisterRequest,
    VerifyOTPRequest,
    ResendOTPRequest,
    AuthResponse,
    UserResponse,
    TokenRefreshRequest
)
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> UserResponse:
    """
    Dependency to get current user from token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    user = await auth_service.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user

# ─── Public Routes ─────────────────────────────────────

@router.post("/register")
async def register(request: UserRegisterRequest):
    """
    Register a new user by sending OTP to email
    """
    result = await auth_service.send_otp(request.email)
    return result

@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest) -> AuthResponse:
    """
    Verify OTP and complete registration/login
    """
    result = await auth_service.verify_otp(request.email, request.otp)
    return result

@router.post("/login")
async def login(request: UserRegisterRequest):
    """
    Login existing user by sending OTP to email
    (Same as register - Supabase handles both)
    """
    result = await auth_service.send_otp(request.email)
    return result

@router.post("/resend-otp")
async def resend_otp(request: ResendOTPRequest):
    """
    Resend OTP to email
    """
    result = await auth_service.send_otp(request.email)
    return result

@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest) -> AuthResponse:
    """
    Refresh access token using refresh token
    """
    result = await auth_service.refresh_token(request.refresh_token)
    return result

# ─── Protected Routes ─────────────────────────────────

@router.get("/me")
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Get current user profile
    """
    return current_user

@router.post("/logout")
async def logout(
    authorization: Optional[str] = Header(None)
):
    """
    Logout current user
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    result = await auth_service.logout(token)
    return result
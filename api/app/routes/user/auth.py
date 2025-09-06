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

# ─── Registration Flow ──────────────────────────────────────────────

@router.post("/register/send-otp")
async def send_registration_otp(request: UserRegisterRequest):
    """
    Step 1: Send OTP for new user registration
    - Checks if user already exists
    - If exists, returns error asking user to login
    - If not exists, sends 4-digit OTP to email
    """
    result = await auth_service.send_registration_otp(request.email)
    return result

@router.post("/register/verify-otp")
async def verify_registration_otp(request: VerifyOTPRequest) -> AuthResponse:
    """
    Step 2: Verify OTP and complete registration
    - Verifies the 4-digit OTP
    - Creates new user account in Supabase
    - Creates user profile in database
    - Returns access token and user info
    """
    result = await auth_service.verify_registration_otp(request.email, request.otp)
    return result

# ─── Login Flow ─────────────────────────────────────────────────────

@router.post("/login/send-otp")
async def send_login_otp(request: UserRegisterRequest):
    """
    Step 1: Send OTP for existing user login
    - Checks if user exists
    - If not exists, returns error asking user to register
    - If exists, sends 4-digit OTP to email
    """
    result = await auth_service.send_login_otp(request.email)
    return result

@router.post("/login/verify-otp")
async def verify_login_otp(request: VerifyOTPRequest) -> AuthResponse:
    """
    Step 2: Verify OTP and complete login
    - Verifies the 4-digit OTP
    - Updates last login timestamp
    - Returns access token and user info
    """
    result = await auth_service.verify_login_otp(request.email, request.otp)
    return result

# ─── Common Auth Routes ─────────────────────────────────────────────

@router.post("/check-email")
async def check_email_exists(request: UserRegisterRequest):
    """
    Check if email exists in system
    - Returns user_exists: true/false
    - Frontend can use this to show appropriate flow
    """
    user_exists = await auth_service.check_user_exists(request.email)
    return {
        "email": request.email,
        "user_exists": user_exists,
        "suggested_action": "login" if user_exists else "register"
    }

@router.post("/resend-otp")
async def resend_otp(request: ResendOTPRequest):
    """
    Resend OTP to email
    - Can be used for both registration and login flows
    - Frontend should specify which flow this is for
    """
    # You might want to track whether this is for login or register
    # For now, treating as login OTP
    result = await auth_service.send_login_otp(request.email)
    return result

@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest) -> AuthResponse:
    """
    Refresh access token using refresh token
    """
    result = await auth_service.refresh_token(request.refresh_token)
    return result

# ─── Protected Routes ───────────────────────────────────────────────

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
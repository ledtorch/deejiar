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
    print("[get_current_user]")
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

# Step 1: Send OTP for new user registration
@router.post("/register/send-otp")
async def send_registration_otp(request: UserRegisterRequest):
    print("[🌐/routes/user/auth/register/send-otp]")
    result = await auth_service.send_registration_otp(request.email)
    return result

# Step 2: Verify OTP and complete registration
@router.post("/register/verify-otp")
async def verify_registration_otp(request: VerifyOTPRequest) -> AuthResponse:
    print("[🌐/routes/user/auth/register/verify-otp]")
    result = await auth_service.verify_registration_otp(request.email, request.otp)
    return result

# ─── Login Flow ─────────────────────────────────────────────────────

@router.post("/login/send-otp")
async def send_login_otp(request: UserRegisterRequest):
    print("[🌐/routes/user/auth/login/send-otp]")
    result = await auth_service.send_login_otp(request.email)
    return result

# Step 2: Verify OTP and complete login
@router.post("/login/verify-otp")
async def verify_login_otp(request: VerifyOTPRequest) -> AuthResponse:
    print("[🌐/routes/user/auth/login/verify-otp]")
    result = await auth_service.verify_login_otp(request.email, request.otp)
    return result

# ─── Common Auth Routes ─────────────────────────────────────────────

@router.post("/check-email")
async def check_email_exists(request: UserRegisterRequest):
    print("[🌐/routes/user/auth/check-email]")
    
    # Dict response from check_user_exists
    user_info = await auth_service.check_user_exists(request.email)
    
    # Extract the boolean from the dict
    user_exists = user_info['user_exists']

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
    result = await auth_service.send_login_otp(request.email)
    return result

@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest) -> AuthResponse:
    print("[🌐/routes/user/auth/refresh]")
    result = await auth_service.refresh_token(request.refresh_token)
    return result

# ─── Protected Routes ───────────────────────────────────────────────

@router.get("/me")
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    print("[🌐/routes/user/auth/me]")
    try:
        from app.db.supabase import get_supabase_admin_client
        
        supabase = get_supabase_admin_client()
        
        # Query fresh user data from Supabase
        result = supabase.table('users') \
            .select('*') \
            .eq('uid', current_user.uid) \
            .single() \
            .execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # 🔍 DEBUG: Log what we're returning
        print("[🐍/routes/user/auth/me] Fresh user data from Supabase:")
        print(f" - UID: {result.data.get('uid')}")
        print(f" - Email: {result.data.get('email')}")
        print(f" - Premium: {result.data.get('premium')}")
        print(f" - Subscription Status: {result.data.get('subscription_status')}")
        
        return result.data
        
    except Exception as e:
        print(f"❌ Error fetching user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user profile: {str(e)}"
        )

@router.post("/logout")
async def logout(
    authorization: Optional[str] = Header(None)
):
    print("[🌐/routes/user/auth/logout]")
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

@router.delete("/delete")
async def delete_account(
    authorization: Optional[str] = Header(None)
):
    print("[🌐/routes/user/auth/delete]")
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
    
    result = await auth_service.delete_account(token)
    return result
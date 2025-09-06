import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from supabase import Client
from gotrue.errors import AuthError

from app.db.supabase import get_supabase_client, get_supabase_admin_client
from app.models.user import (
    UserProfile, 
    UserResponse, 
    AuthResponse,
    AuthProvider
)

class AuthService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.admin_supabase = get_supabase_admin_client()
    
    async def check_user_exists(self, email: str) -> bool:
        """
        Check if user already exists in Supabase Auth
        """
        try:
            # Query the users table to see if email exists
            result = self.admin_supabase.auth.admin.list_users()
            
            # Check if any user has this email
            for user in result:
                if user.email == email and user.email_confirmed_at is not None:
                    return True
            return False
            
        except Exception as e:
            print(f"Error checking user existence: {str(e)}")
            return False
    
    async def send_registration_otp(self, email: str) -> Dict[str, str]:
        """
        Send OTP for new user registration
        """
        try:
            # First check if user already exists
            user_exists = await self.check_user_exists(email)
            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists. Please use login instead."
                )
            
            # Send OTP for registration
            response = self.supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "should_create_user": True,
                    "data": {
                        "provider": AuthProvider.EMAIL.value,
                        "registered_at": datetime.utcnow().isoformat(),
                        "registration_flow": True
                    }
                }
            })
            
            return {
                "message": "Registration OTP sent successfully",
                "email": email,
                "action": "register"
            }
            
        except HTTPException:
            raise
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to send registration OTP: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def send_login_otp(self, email: str) -> Dict[str, str]:
        """
        Send OTP for existing user login
        """
        try:
            # Check if user exists
            user_exists = await self.check_user_exists(email)
            if not user_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No account found with this email. Please register first."
                )
            
            # Send OTP for login
            response = self.supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "should_create_user": False,  # Don't create new user
                    "data": {
                        "login_flow": True
                    }
                }
            })
            
            return {
                "message": "Login OTP sent successfully",
                "email": email,
                "action": "login"
            }
            
        except HTTPException:
            raise
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to send login OTP: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def verify_registration_otp(self, email: str, otp: str) -> AuthResponse:
        """
        Verify OTP for registration and create new user profile
        """
        try:
            # Verify OTP with Supabase
            response = self.supabase.auth.verify_otp({
                "email": email,
                "token": otp,
                "type": "email"
            })
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid OTP"
                )
            
            # Generate custom UID for new user
            custom_uid = self._generate_uid()
            
            # Update user metadata with custom UID
            user_metadata = {
                "uid": custom_uid,
                "provider": AuthProvider.EMAIL.value,
                "registered_at": datetime.utcnow().isoformat(),
                "is_new_user": True
            }
            
            update_response = self.admin_supabase.auth.admin.update_user_by_id(
                response.user.id,
                {"user_metadata": user_metadata}
            )
            
            # Create user profile in database
            await self._create_user_profile(
                response.user.id,
                custom_uid,
                email,
                AuthProvider.EMAIL
            )
            
            # Build response
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=UserResponse(
                    uid=custom_uid,
                    email=email,
                    display_name=None,
                    avatar_url=None,
                    provider=AuthProvider.EMAIL,
                    is_new_user=True
                ),
                expires_in=response.session.expires_in
            )
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Registration OTP verification failed: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def verify_login_otp(self, email: str, otp: str) -> AuthResponse:
        """
        Verify OTP for login and return existing user
        """
        try:
            # Verify OTP with Supabase
            response = self.supabase.auth.verify_otp({
                "email": email,
                "token": otp,
                "type": "email"
            })
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid OTP"
                )
            
            # Get existing user metadata
            user_metadata = response.user.user_metadata or {}
            
            if not user_metadata.get("uid"):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User profile incomplete. Please contact support."
                )
            
            # Update last login
            await self._update_last_login(user_metadata.get("uid"))
            
            # Build response
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=UserResponse(
                    uid=user_metadata.get("uid"),
                    email=email,
                    display_name=user_metadata.get("display_name"),
                    avatar_url=user_metadata.get("avatar_url"),
                    provider=AuthProvider(user_metadata.get("provider", "email")),
                    is_new_user=False
                ),
                expires_in=response.session.expires_in
            )
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Login OTP verification failed: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def refresh_token(self, refresh_token: str) -> AuthResponse:
        """
        Refresh access token using refresh token
        """
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            user_metadata = response.user.user_metadata or {}
            
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=UserResponse(
                    uid=user_metadata.get("uid"),
                    email=response.user.email,
                    display_name=user_metadata.get("display_name"),
                    avatar_url=user_metadata.get("avatar_url"),
                    provider=AuthProvider(user_metadata.get("provider", "email")),
                    is_new_user=False
                ),
                expires_in=response.session.expires_in
            )
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token refresh failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def get_user_by_token(self, access_token: str) -> Optional[UserResponse]:
        """
        Get user information from access token
        """
        try:
            response = self.supabase.auth.get_user(access_token)
            
            if not response.user:
                return None
            
            user_metadata = response.user.user_metadata or {}
            
            return UserResponse(
                uid=user_metadata.get("uid"),
                email=response.user.email,
                display_name=user_metadata.get("display_name"),
                avatar_url=user_metadata.get("avatar_url"),
                provider=AuthProvider(user_metadata.get("provider", "email")),
                is_new_user=user_metadata.get("is_new_user", False)
            )
            
        except Exception:
            return None
    
    async def logout(self, access_token: str) -> Dict[str, str]:
        """
        Logout user (invalidate session)
        """
        try:
            self.supabase.auth.sign_out(access_token)
            return {"message": "Logged out successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Logout failed: {str(e)}"
            )
    
    def _generate_uid(self) -> str:
        """
        Generate a unique user ID
        Format: dj_<timestamp>_<random>
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        random_part = str(uuid.uuid4())[:8]
        return f"dj_{timestamp}_{random_part}"
    
    async def _create_user_profile(
        self, 
        supabase_id: str, 
        uid: str, 
        email: str,
        provider: AuthProvider
    ):
        """
        Create new user profile in database
        """
        try:
            self.supabase.table('users').insert({
                'uid': uid,
                'email': email,
                'premium': False,  # Default to non-premium
                'created_at': datetime.utcnow().isoformat(),
                'language': [],  # Empty array for languages
                'age': None,
                'gender': None,
                'x_account': None,
                'ig_account': None
            }).execute()
                
        except Exception as e:
            print(f"Failed to create user profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user profile"
            )
    
    async def _update_last_login(self, uid: str):
        """
        Update user's last login timestamp
        """
        try:
            self.supabase.table('users').update({
                'last_login': datetime.utcnow().isoformat()
            }).eq('uid', uid).execute()
        except Exception as e:
            print(f"Failed to update last login: {str(e)}")

# Singleton instance
auth_service = AuthService()
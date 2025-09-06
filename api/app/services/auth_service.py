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
    
    async def send_otp(self, email: str) -> Dict[str, str]:
        """
        Send OTP to user's email for registration/login
        """
        try:
            # Send OTP using Supabase Auth
            response = self.supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "should_create_user": True,  # Create user if doesn't exist
                    "data": {
                        "provider": AuthProvider.EMAIL.value,
                        "registered_at": datetime.utcnow().isoformat()
                    }
                }
            })
            
            return {
                "message": "OTP sent successfully",
                "email": email
            }
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to send OTP: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def verify_otp(self, email: str, otp: str) -> AuthResponse:
        """
        Verify OTP and complete registration/login
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
            
            # Generate custom UID if user doesn't have one
            user_metadata = response.user.user_metadata or {}
            
            if "uid" not in user_metadata:
                custom_uid = self._generate_uid()
                
                # Update user metadata with custom UID
                update_response = self.admin_supabase.auth.admin.update_user_by_id(
                    response.user.id,
                    {
                        "user_metadata": {
                            **user_metadata,
                            "uid": custom_uid,
                            "provider": AuthProvider.EMAIL.value
                        }
                    }
                )
                user_metadata["uid"] = custom_uid
            
            # Create user profile in custom table if needed
            await self._ensure_user_profile(
                response.user.id,
                user_metadata.get("uid"),
                email,
                AuthProvider.EMAIL
            )
            
            # Build response
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=UserResponse(
                    uid=user_metadata.get("uid"),
                    email=email,
                    display_name=user_metadata.get("display_name"),
                    avatar_url=user_metadata.get("avatar_url"),
                    provider=AuthProvider.EMAIL
                ),
                expires_in=response.session.expires_in
            )
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"OTP verification failed: {str(e)}"
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
                    provider=AuthProvider(user_metadata.get("provider", "email"))
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
                provider=AuthProvider(user_metadata.get("provider", "email"))
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
    
    async def _ensure_user_profile(
        self, 
        supabase_id: str, 
        uid: str, 
        email: str,
        provider: AuthProvider
    ):
        """
        Ensure user profile exists in custom table
        You'll need to create a 'user_profiles' table in Supabase
        """
        try:
            # Check if profile exists
            result = self.supabase.table('user_profiles').select("*").eq('uid', uid).execute()
            
            if not result.data:
                # Create profile
                self.supabase.table('user_profiles').insert({
                    'supabase_id': supabase_id,
                    'uid': uid,
                    'email': email,
                    'provider': provider.value,
                    'created_at': datetime.utcnow().isoformat(),
                    'last_login': datetime.utcnow().isoformat()
                }).execute()
            else:
                # Update last login
                self.supabase.table('user_profiles').update({
                    'last_login': datetime.utcnow().isoformat()
                }).eq('uid', uid).execute()
                
        except Exception as e:
            # Log error but don't fail authentication
            print(f"Failed to ensure user profile: {str(e)}")

# Singleton instance
auth_service = AuthService()
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
    
    def _create_user_response_from_data(self, user_data: Dict) -> UserResponse:
        """Helper method to create UserResponse from database data"""
        return UserResponse(
            # Auth
            provider=AuthProvider.EMAIL,
            is_new_user=user_data.get('is_new_user', False),

            # Basic info
            uid=user_data.get('uid'),
            email=user_data.get('email'),
            display_name=user_data.get('display_name'),
            avatar_url=user_data.get('avatar_url'),
            created_at=user_data.get('created_at'),

            # Social account info
            x_account=user_data.get('x-account'),
            x_connected=user_data.get('x-connected'),
            ig_account=user_data.get('ig-account'),
            ig_connected=user_data.get('ig-connected'),

            # Subscription info
            premium=user_data.get('premium', False),

            # 🏗️ TODO: Future plan
            language=user_data.get('language', []),
            age=user_data.get('age'),
            gender=user_data.get('gender'),
        )
    
    async def check_user_exists(self, email: str) -> Dict[str, any]:
        try:
            print(f"[check_user_exists] Checking email: {email}")
            
            result = self.supabase.table('users') \
                .select('uid, account_status') \
                .eq('email', email) \
                .execute()
            
            # No data found = user doesn't exist
            if not result.data or len(result.data) == 0:
                print(f"[check_user_exists] ❌ User not found")
                return {
                    'user_exists': False,
                    'account_status': None,
                    'uid': None
                }

            # Get user data
            user = result.data[0]
            uid = user.get('uid')
            account_status = user.get('account_status', 'active')
            
            print(f"[check_user_exists] ✅ User found!")
            print(f"  - UID: {uid}")
            print(f"  - Account Status: {account_status}")
            
            return {
                'user_exists': True,
                'account_status': account_status,
                'uid': uid
            }
            
        except Exception as e:
            print(f"[check_user_exists] ❌ Error: {str(e)}")
            return {
                'user_exists': False,
                'account_status': None,
                'uid': None
            }

    # ─── Registration ───────────────────────────────────────────────────
    async def send_registration_otp(self, email: str) -> Dict[str, str]:
        """Send 6-digit OTP for new user registration"""
        try:
            # Check if user already exists
            user_exists = await self.check_user_exists(email)
            if user_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists. Please use login instead."
                )
            
            # Send OTP using Supabase's sign_in_with_otp
            response = self.supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "should_create_user": True,
                    "data": {
                        "provider": AuthProvider.EMAIL.value,
                        "registration_flow": True
                    }
                }
            })
            
            return {
                "message": "6-digit verification code sent to your email",
                "email": email,
                "action": "register",
                "expires_in": 600  # 10 minutes
            }
            
        except HTTPException:
            raise
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to send verification code: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )

    async def verify_registration_otp(self, email: str, otp: str) -> AuthResponse:
        """Verify 6-digit OTP for registration and create user profile"""
        try:
            # Verify OTP with Supabase
            response = self.supabase.auth.verify_otp({
                "email": email,
                "token": otp,
                "type": "email"  # This is for email OTP verification
            })
            
            if not response.user or not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid verification code"
                )
            
            # Generate custom UID (simplified)
            custom_uid = self._generate_uid()
            
            # Create user profile in YOUR database table
            # We do this FIRST before updating metadata to avoid orphaned auth users
            user_data = await self._create_user_profile(
                response.user.id,
                custom_uid,
                email,
                AuthProvider.EMAIL
            )
            
            # Update user metadata in Supabase Auth (optional, can skip if fails)
            user_metadata = {
                "uid": custom_uid,
                "provider": AuthProvider.EMAIL.value,
                "created_at": datetime.utcnow().isoformat(),
                "is_new_user": True
            }
            
            try:
                self.admin_supabase.auth.admin.update_user_by_id(
                    response.user.id,
                    {"user_metadata": user_metadata}
                )
            except Exception as e:
                print(f"Warning: Failed to update user metadata: {str(e)}")
                # Continue anyway, the user record is created
            
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=self._create_user_response_from_data({
                    **user_data,
                    'is_new_user': True
                }),
                expires_in=response.session.expires_in if hasattr(response.session, 'expires_in') else 3600
            )
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid verification code: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            print(f"Registration error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )
    
    # ─── Login ──────────────────────────────────────────────────────────
    async def send_login_otp(self, email: str) -> Dict[str, str]:
        try:
            # Check if user exists
            user_exists = await self.check_user_exists(email)
            if not user_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No account found with this email. Please register first."
                )
            
            # Send OTP for existing user
            response = self.supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "should_create_user": False,
                    "data": {
                        "login_flow": True
                    }
                }
            })
            
            return {
                "message": "6-digit verification code sent to your email",
                "email": email,
                "action": "login",
                "expires_in": 600  # 10 minutes
            }
            
        except HTTPException:
            raise
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to send verification code: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    async def verify_login_otp(self, email: str, otp: str) -> AuthResponse:
        """Verify 6-digit OTP for login"""
        try:
            # Verify OTP with Supabase
            response = self.supabase.auth.verify_otp({
                "email": email,
                "token": otp,
                "type": "email"
            })
            
            if not response.user or not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid verification code"
                )
            
            # Get user from YOUR database
            user_data = await self._get_user_profile(email)
            
            if not user_data:
                # User exists in Auth but not in database - create profile
                custom_uid = self._generate_uid()
                user_data = await self._create_user_profile(
                    response.user.id,
                    custom_uid,
                    email,
                    AuthProvider.EMAIL
                )
            
            # Update last login
            await self._update_last_login(user_data['uid'])
            
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=self._create_user_response_from_data({
                    **user_data,
                    'is_new_user': False
                }),
                expires_in=response.session.expires_in if hasattr(response.session, 'expires_in') else 3600
            )
            
        except AuthError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid verification code: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(e)}"
            )
    
    # ─── Logout ──────────────────────────────────────────────────────────
    async def logout(self, token: str) -> Dict[str, str]:
        """Logout user by invalidating the session"""
        try:
            # Sign out from Supabase
            self.supabase.auth.sign_out()
            
            return {
                "message": "Successfully logged out"
            }
        except Exception as e:
            print(f"Logout error: {str(e)}")
            # Even if logout fails, we return success
            # Frontend will clear tokens anyway
            return {
                "message": "Logged out"
            }
    
    # ─── Delete account ──────────────────────────────────────────────────
    async def delete_account(self, token: str) -> Dict[str, str]:
        """
        Schedule account for deletion (30-day grace period)
        """
        try:
            print(f"[delete_account] 1️⃣ Received token: {token[:20]}...")
            
            # Get user from token
            user = await self.get_user_by_token(token)
            if not user:
                print(f"[delete_account] ❌ Failed to get user from token")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            
            print(f"[delete_account] 2️⃣ User found: {user.uid}")
            
            # Get current user data
            print(f"[delete_account] 3️⃣ Fetching user data from database...")
            result = self.supabase.table('users') \
                .select('*') \
                .eq('uid', user.uid) \
                .single() \
                .execute()
            
            if not result.data:
                print(f"[delete_account] ❌ User data not found in database")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user_data = result.data
            print(f"[delete_account] 4️⃣ Current user data retrieved")
            print(f"  - UID: {user_data.get('uid')}")
            print(f"  - Email: {user_data.get('email')}")
            print(f"  - Account Status: {user_data.get('account_status')}")
            
            # Check if already pending deletion
            if user_data.get('account_status') == 'pending_deletion':
                deletion_date = user_data.get('deletion_scheduled_at')
                print(f"[delete_account] ⚠️ Account already pending deletion: {deletion_date}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Account deletion already scheduled for {deletion_date}"
                )
            
            # ⭐ Calculate deletion date
            now = datetime.utcnow()
            deletion_date = now  # Testing: immediate deletion
            
            # deletion_date = deletion_date.replace(
            #     hour=23, 
            #     minute=59, 
            #     second=0, 
            #     microsecond=0
            # )
            
            print(f"[delete_account] 5️⃣ Deletion date calculated: {deletion_date.isoformat()}")
            
            # Check subscription
            has_active_subscription = (
                user_data.get('premium') and 
                user_data.get('subscription_status') in ['active', 'trial']
            )
            
            if has_active_subscription:
                print(f"[delete_account] 6️⃣ ⚠️ Active subscription detected")
                print(f"  - Plan: {user_data.get('subscription_plan')}")
                print(f"  - Status: {user_data.get('subscription_status')}")
            else:
                print(f"[delete_account] 6️⃣ No active subscription")
            
            # Prepare update data
            update_data = {
                'account_status': 'pending_deletion',
                'deletion_requested_at': now.isoformat(),
                'deletion_scheduled_at': deletion_date.isoformat(),
                'subscription_status': 'cancelled' if has_active_subscription else user_data.get('subscription_status')
            }
            
            print(f"[delete_account] 7️⃣ Updating database with:")
            print(f"  {update_data}")
            
            # Execute update
            update_result = self.admin_supabase.table('users').update(update_data).eq('uid', user.uid).execute()
            
            if not update_result.data:
                print(f"[delete_account] ❌ Database update returned no data")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to schedule account deletion"
                )
            
            print(f"[delete_account] 8️⃣ ✅ Database updated successfully")
            print(f"[delete_account] 9️⃣ ✅ Deletion scheduled for: {deletion_date.isoformat()}")
            
            # 🧪 TESTING: Actually delete the user immediately
            TESTING_IMMEDIATE_DELETE = True  # Set to False for production
            
            if TESTING_IMMEDIATE_DELETE:
                print(f"[delete_account] 🧪 TESTING MODE: Deleting user immediately...")
                
                # Delete from users table
                delete_result = self.admin_supabase.table('users') \
                    .delete() \
                    .eq('uid', user.uid) \
                    .execute()
                
                print(f"[delete_account] ✅ User deleted from database")
                
                # Delete from Supabase Auth
                try:
                    auth_users = self.admin_supabase.auth.admin.list_users()
                    auth_user = next((u for u in auth_users if u.email == user_data['email']), None)
                    
                    if auth_user:
                        self.admin_supabase.auth.admin.delete_user(auth_user.id)
                        print(f"[delete_account] ✅ User deleted from Supabase Auth: {auth_user.id}")
                    else:
                        print(f"[delete_account] ⚠️ Auth user not found for email: {user_data['email']}")
                except Exception as e:
                    print(f"[delete_account] ⚠️ Auth deletion error: {str(e)}")
                
                return {
                    "message": "Account deleted immediately (TESTING MODE)",
                    "deleted_at": now.isoformat(),
                    "note": "User has been permanently deleted"
                }
            
            return {
                "message": "Account deletion scheduled successfully",
                "deletion_requested_at": now.isoformat(),
                "deletion_scheduled_at": deletion_date.isoformat(),
                "recovery_email": "hi@deejiar.com",
                "note": "You cannot log in during the deletion grace period. To recover your account, email hi@deejiar.com before the deadline."
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"[delete_account] ❌ Unexpected error occurred")
            print(f"[delete_account] Error type: {type(e).__name__}")
            print(f"[delete_account] Error message: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete account: {str(e)}"
            )


    # Others
    async def get_user_by_token(self, token: str) -> Optional[UserResponse]:
        """Get user information from access token"""
        try:
            # Get user from Supabase using the token
            user_response = self.supabase.auth.get_user(token)
            
            if not user_response or not user_response.user:
                return None
            
            # Get user profile from database
            user_data = await self._get_user_profile(user_response.user.email)
            
            if not user_data:
                return None
            
            return self._create_user_response_from_data(user_data)
            
        except Exception as e:
            print(f"Error getting user by token: {str(e)}")
            return None
    
    async def refresh_token(self, refresh_token: str) -> AuthResponse:
        """Refresh access token using refresh token"""
        try:
            # Refresh the session
            response = self.supabase.auth.refresh_session(refresh_token)
            
            if not response.user or not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            # Get user profile from database
            user_data = await self._get_user_profile(response.user.email)
            
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User profile not found"
                )
            
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                user=self._create_user_response_from_data(user_data),
                expires_in=response.session.expires_in if hasattr(response.session, 'expires_in') else 3600
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token refresh failed: {str(e)}"
            )
    
    def _generate_uid(self) -> str:
        """Generate unique user ID"""
        random_part = str(uuid.uuid4())[:8]
        return f"{random_part}"
    
    async def _create_user_profile(
        self, 
        supabase_id: str, 
        uid: str, 
        email: str,
        provider: AuthProvider
    ) -> Dict:
        """Create user profile in YOUR database and return the created data"""
        try:
            profile_data = {
                'uid': uid,
                'email': email,
                'premium': False,
                'created_at': datetime.utcnow().isoformat(),
                'language': [],
                'age': None,
                'gender': None,
                'x-account': None,
                'ig-account': None,
                'x-connected': None,
                'ig-connected': None
            }
            
            result = self.supabase.table('users').insert(profile_data).execute()
            
            if not result.data:
                raise Exception("Failed to insert user profile")
                
            print(f"✅ User profile created successfully: {uid}")
            return result.data[0]  # Return the created user data
            
        except Exception as e:
            print(f"❌ Failed to create user profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user profile: {str(e)}"
            )
    
    async def _get_user_profile(self, email: str) -> Optional[Dict]:
        """Get user profile from YOUR database"""
        try:
            result = self.supabase.table('users').select('*').eq('email', email).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            
            return None
            
        except Exception as e:
            print(f"Error getting user profile: {str(e)}")
            return None
    
    async def _update_last_login(self, uid: str):
        """Update user's last login timestamp"""
        try:
            self.supabase.table('users').update({
                'last_login': datetime.utcnow().isoformat()
            }).eq('uid', uid).execute()
        except Exception as e:
            print(f"Failed to update last login: {str(e)}")

# Singleton instance
auth_service = AuthService()
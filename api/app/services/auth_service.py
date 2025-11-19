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

from app.utils.token_tracker import token_tracker

class AuthService:
    def __init__(self):
        pass
    
    @property
    def supabase(self) -> Client:
        return get_supabase_client()
    
    @property
    def admin_supabase(self) -> Client:
        return get_supabase_admin_client()

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
            
            result = self.admin_supabase.table('users') \
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

    # ─── Refresh Token ─────────────────────────────────────────────────────
    async def refresh_token(self, refresh_token: str) -> AuthResponse:
        print("[🛠️/services/auth_service/refresh_token]")
        print(f"📥 Old Token (received from frontend): {refresh_token}")
        
        # Save the old token for comparison
        old_token = refresh_token
        
        # 🔍 CHECK: Has this token been used before?
        is_reused, usage_count = token_tracker.check_for_reuse(old_token)
        
        if is_reused:
            print(f"⚠️ WARNING: This Old Token has been used {usage_count} time(s) before!")
            print(f"⚠️ This refresh attempt will likely fail with 'Already Used'")
            token_tracker.print_token_history(old_token)
        
        # 🔍 LOG: Token refresh attempt
        token_tracker.log_usage(
            old_token, 
            "REFRESH_ATTEMPT",
            "pending",
            f"Attempt #{usage_count + 1}"
        )
        
        try:
            if not refresh_token:
                token_tracker.log_usage(old_token, "REFRESH_ATTEMPT", "failed", "No token provided")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Refresh token required"
                )
            
            print("1️⃣ Calling supabase.auth.refresh_session()...")
            
            # Try refreshing the session
            response = self.supabase.auth.refresh_session(refresh_token)
            
            print(f"2️⃣ Response received: {type(response)}")
            print(f"3️⃣ Has user: {response.user is not None if response else False}")
            print(f"4️⃣ Has session: {response.session is not None if response else False}")
            
            if not response.user or not response.session:
                print("❌ No user or session in response")
                token_tracker.log_usage(old_token, "REFRESH_ATTEMPT", "failed", "No session in response")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token - no session returned"
                )
            
            print(f"5️⃣ Getting user profile for: {response.user.email}")
            
            # ✅ IMPORTANT: Get user profile from database
            user_data = await self._get_user_profile(response.user.email)
            
            if not user_data:
                print("❌ User profile not found in database")
                token_tracker.log_usage(old_token, "REFRESH_ATTEMPT", "failed", "User not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User profile not found"
                )
            
            # Get the new token from Supabase
            current_token = response.session.refresh_token
            
            # 🔍 CRITICAL: Check token usage status
            old_token_is_reused, old_usage_count = token_tracker.check_for_reuse(old_token)
            current_token_is_used, current_usage_count = token_tracker.check_for_reuse(current_token)
            
            print("✅ Token refresh successful!")
            print(f"6️⃣ Token Status:")
            print(f"   📥 Old Token: {old_token}")
            print(f"      - Old Token Used: {old_token_is_reused} (used {old_usage_count} time(s))")
            print(f"   📤 Current Token: {current_token}")
            print(f"      - Current Token Used: {current_token_is_used} (used {current_usage_count} time(s))")
            print(f"   🔄 Tokens Are Different: {current_token != old_token}")
            
            # Check for issues
            if current_token == old_token:
                print("🚨 CRITICAL BUG: Supabase returned the SAME token!")
                print("🚨 This will cause 'Already Used' error on next refresh!")
                token_tracker.log_usage(
                    old_token, 
                    "REFRESH_ATTEMPT", 
                    "success_but_same_token",
                    "Backend returned same token - this is a bug!"
                )
            else:
                print("✅ GOOD: Received new Current Token from Supabase")
                print(f"   ✅ Old Token ({old_token}) should NOT be used again")
                print(f"   ✅ Current Token ({current_token}) should be used for next refresh")
                
                # Log the old token as successfully used
                token_tracker.log_usage(
                    old_token, 
                    "REFRESH_ATTEMPT", 
                    "success",
                    f"Replaced with Current Token: {current_token}"
                )
                
                # Log the new Current Token as issued
                token_tracker.log_usage(
                    current_token, 
                    "TOKEN_ISSUED", 
                    "issued",
                    f"Replaced Old Token: {old_token}"
                )
            
            return AuthResponse(
                access_token=response.session.access_token,
                refresh_token=current_token,
                user=self._create_user_response_from_data(user_data),
                expires_in=response.session.expires_in if hasattr(response.session, 'expires_in') else 3600
            )
            
        except HTTPException:
            raise
        except AuthError as e:
            error_msg = str(e)
            print(f"❌ Supabase AuthError: {type(e).__name__}")
            print(f"❌ Error message: {error_msg}")
            
            # 🔍 LOG: Failed refresh
            if "Already Used" in error_msg:
                token_tracker.log_usage(old_token, "REFRESH_ATTEMPT", "already_used", error_msg)
                print("🚨 'Already Used' error detected!")
                print(f"🚨 The Old Token ({old_token}) was already used before")
                print("🚨 Printing complete token history:")
                token_tracker.print_token_history(old_token)
            else:
                token_tracker.log_usage(old_token, "REFRESH_ATTEMPT", "auth_error", error_msg)
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token refresh failed: {error_msg}"
            )
        except Exception as e:
            print(f"❌ Unexpected error: {type(e).__name__}")
            print(f"❌ Error message: {str(e)}")
            token_tracker.log_usage(old_token, "REFRESH_ATTEMPT", "exception", str(e))
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token refresh failed: {str(e)}"
            )

    # ─── Registration ───────────────────────────────────────────────────
    async def send_registration_otp(self, email: str) -> Dict[str, str]:
        try:
            # Check if user exists and get account status
            result = self.supabase.table('users') \
                .select('uid, account_status') \
                .eq('email', email) \
                .execute()
            
            if result.data and len(result.data) > 0:
                user = result.data[0]
                account_status = user.get('account_status', 'active')
                
                # ⚠️ Block registration if account is active
                if account_status == 'active':
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="User with this email already exists. Please use login instead."
                    )
                
                # ⚠️ Block registration if account is pending deletion
                if account_status == 'pending_deletion':
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            
            # Send OTP
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
                "expires_in": 600
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
            
            # Check if user already exists
            existing_user = await self._get_user_profile(email)

            if existing_user:
                print(f"[verify_registration_otp] ⚠️ User already exists: {email}")
                
                return AuthResponse(
                    access_token=response.session.access_token,
                    refresh_token=response.session.refresh_token,
                    user=self._create_user_response_from_data({
                        **existing_user,
                        'is_new_user': False
                    }),
                    expires_in=response.session.expires_in if hasattr(response.session, 'expires_in') else 3600
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
            # Check if user exists and get account status
            result = self.supabase.table('users') \
                .select('uid, account_status') \
                .eq('email', email) \
                .execute()
            
            if not result.data or len(result.data) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No account found with this email. Please register first."
                )
            
            user = result.data[0]
            account_status = user.get('account_status', 'active')
            
            # ⚠️ Block login if account is pending deletion
            if account_status == 'pending_deletion':
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            
            # Send OTP for existing user
            print(f"[send_login_otp] Sending OTP to: {email}")
            
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
                "expires_in": 600
            }
            
        except HTTPException:
            raise
        except AuthError as e:
            print(f"[send_login_otp] AuthError: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to send verification code: {str(e)}"
            )
        except Exception as e:
            print(f"[send_login_otp] Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
        
    async def verify_login_otp(self, email: str, otp: str) -> AuthResponse:
        try:
            # Verify OTP with Supabase
            response = self.supabase.auth.verify_otp({
                "email": email,
                "token": otp,
                "type": "email"
            })

            # 🔍 ADD THIS DEBUG - Check what Supabase returns
            print("=" * 50)
            print("🔍 [verify_login_otp] Supabase Response:")
            print(f"  Response type: {type(response)}")
            print(f"  Has user: {response.user is not None}")
            print(f"  Has session: {response.session is not None}")
            
            if response.session:
                print(f"  📊 Session details:")
                print(f"    Access Token Length: {len(response.session.access_token)}")
                print(f"    Refresh Token Length: {len(response.session.refresh_token)}")
                print(f"    Refresh Token Value: {response.session.refresh_token}")
                print(f"    Refresh Token Type: {type(response.session.refresh_token)}")
            print("=" * 50)
            # 🔍 END DEBUG
            
            if not response.user or not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid verification code"
                )
            
            # Get user from YOUR database
            user_data = await self._get_user_profile(email)
            
            if not user_data:
                print(f"[verify_login_otp] ❌ No user found in database for {email}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found. Please register first."
                )
            
            # Check if account is pending deletion
            if user_data.get('account_status') == 'pending_deletion':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This account is scheduled for deletion."
                )

            # Update last login
            await self._update_last_login(user_data['uid'])
            
            # 🔍 DEBUG - Track initial token issuance
            initial_token = response.session.refresh_token
            token_tracker.log_usage(
                initial_token,
                "TOKEN_ISSUED",
                "login",
                f"Initial token issued during login for: {email}"
            )

            print(f"📝 [verify_login_otp] Initial refresh token issued: {initial_token}")
            print(f"📝 [verify_login_otp] User should use this token for first refresh")
            # 🔍 END DEBUG

            # 🔍 DEBUG - Check what we're about to return
            print("🔍 [verify_login_otp] About to return AuthResponse:")
            print(f"  Access Token Length: {len(response.session.access_token)}")
            print(f"  Refresh Token Length: {len(response.session.refresh_token)}")
            print(f"  Refresh Token: {response.session.refresh_token}")
            # 🔍 END DEBUG

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
            """ 
            ⚠️ Use anon client to update public.users
            Admin client is SERVICE_ROLE, this can NOT read auth.data() to verify POLICIES
            """
            update_result = self.supabase.table('users').update(update_data).eq('uid', user.uid).execute()
            if not update_result.data:
                print(f"[delete_account] ❌ Database update returned no data")
                print(f" - raw result: {update_result}")
                print(f" - data: {update_result.data}")
                print(f" - error: {getattr(update_result, 'error', None)}")
                print(f" - status_code: {getattr(update_result, 'status_code', None)}")
                print(f" - count: {getattr(update_result, 'count', None)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to schedule account deletion"
                )
            
            print(f"[delete_account] 8️⃣ ✅ Database updated successfully")
            
            # 🧪 TESTING: Delete the user immediately
            print(f"[delete_account] 🗑️ Deleting user immediately...")

            # Delete from users table
            delete_result = self.supabase.table('users').delete().eq('uid', user.uid).execute()

            rows_affected = len(delete_result.data) if delete_result.data else 0
            print(f"[delete_account] ✅ User deleted from public.users")
            print(f"  - Rows affected: {rows_affected}")

            if rows_affected == 0:
                print(f"[delete_account] ⚠️ Warning: No rows deleted from public.users")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete user profile (RLS policy blocking or no matching record)"
                )

            # try:
            #     # Get auth user
            #     auth_users = self.supabase.auth.admin.list_users()
            #     auth_user = next((u for u in auth_users if u.email == user_data['email']), None)
                
            #     if auth_user:
            #         print(f"[delete_account] 🗑️ Deleting auth user: {auth_user.id}")
                    
            #         # Try API deletion first
            #         try:
            #             # self.supabase.auth.admin.delete_user(auth_user.id)
            #             self.admin_supabase.auth.admin.delete_user(auth_user.id)
            #             print(f"[delete_account] ✅ User deleted from auth.users via API")
            #         except Exception as api_error:
            #             # If API fails, try SQL function
            #             print(f"[delete_account] ⚠️ API deletion failed: {str(api_error)}")
            #             print(f"[delete_account] 🔄 Trying SQL function fallback...")
                        
            #             sql_result = self.admin_supabase.rpc(
            #                 'delete_auth_user',
            #                 {'user_id': str(auth_user.id)}
            #             ).execute()
                        
            #             if sql_result.data and sql_result.data.get('success'):
            #                 print(f"[delete_account] ✅ User deleted from auth.users via SQL")
            #             else:
            #                 error_msg = sql_result.data.get('message', 'Unknown error') if sql_result.data else 'No response'
            #                 raise Exception(f"Both API and SQL deletion failed. SQL error: {error_msg}")
            #     else:
            #         print(f"[delete_account] ⚠️ Auth user not found for email: {user_data['email']}")
                    
            # except Exception as e:
            #     error_msg = str(e)
            #     print(f"[delete_account] ❌ Auth deletion error: {error_msg}")
                
            #     # CRITICAL: public.users deleted but auth.users failed
            #     # This is a GDPR compliance issue
            #     raise HTTPException(
            #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #         detail=f"Failed to fully delete account (GDPR compliance): {error_msg}"
            #     )

            # Around line 682-691, replace with:
            print(f"[delete_account] 🔍 Checking admin client configuration...")
            print(f"  - Client type: {type(self.admin_supabase)}")
            print(f"  - Has auth: {hasattr(self.admin_supabase, 'auth')}")
            print(f"  - Has admin: {hasattr(self.admin_supabase.auth, 'admin')}")

            try:
                # List users first to verify admin access works
                print(f"[delete_account] 🔍 Testing admin.list_users()...")
                auth_users = self.admin_supabase.auth.admin.list_users()
                print(f"[delete_account] ✅ list_users() worked! Found {len(auth_users)} users")
                
                auth_user = next((u for u in auth_users if u.email == user_data['email']), None)
                
                if auth_user:
                    print(f"[delete_account] 🗑️ Found auth user:")
                    print(f"  - ID: {auth_user.id}")
                    print(f"  - Email: {auth_user.email}")
                    print(f"  - Created: {auth_user.created_at}")
                    
                    # Try to get user details first
                    print(f"[delete_account] 🔍 Testing admin.get_user_by_id()...")
                    try:
                        user_details = self.admin_supabase.auth.admin.get_user_by_id(auth_user.id)
                        print(f"[delete_account] ✅ get_user_by_id() worked!")
                        print(f"  - Can read user: {user_details.email}")
                    except Exception as get_error:
                        print(f"[delete_account] ❌ get_user_by_id() failed: {str(get_error)}")
                    
                    # Now try delete
                    print(f"[delete_account] 🗑️ Calling admin.delete_user()...")
                    print(f"  - User ID: {auth_user.id}")
                    print(f"  - Using client: admin_supabase")
                    
                    delete_response = self.admin_supabase.auth.admin.delete_user(auth_user.id)
                    
                    print(f"[delete_account] ✅ Delete response: {delete_response}")
                    print(f"[delete_account] ✅ User deleted from auth.users!")
                    
                else:
                    print(f"[delete_account] ⚠️ Auth user not found for email: {user_data['email']}")
                    
            except Exception as e:
                print(f"[delete_account] ❌ Auth deletion error: {str(e)}")
                print(f"  - Error type: {type(e).__name__}")
                print(f"  - Error details: {e.__dict__ if hasattr(e, '__dict__') else 'N/A'}")
                
                # Check if it's an API error with status code
                if hasattr(e, 'status'):
                    print(f"  - HTTP Status: {e.status}")
                if hasattr(e, 'code'):
                    print(f"  - Error code: {e.code}")
                
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to delete auth user: {str(e)}"
                )
            # End of auth deletion

            print(f"[delete_account] ✅ Account fully deleted")

            return {
                "message": "Account deleted successfully",
                "deleted_at": now.isoformat(),
                "note": "Your account has been permanently deleted from all systems"
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
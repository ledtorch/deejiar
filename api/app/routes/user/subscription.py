from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.routes.user.auth import get_current_user
from app.models.user import UserResponse
from app.db.supabase import get_supabase_client, get_supabase_admin_client

router = APIRouter(prefix="/subscription", tags=["Subscription"])

class SyncPremiumRequest(BaseModel):
    subscription_plan: str  # e.g., "com.deejiar.premium.brass.yearly.v1"
    subscription_status: str = "active"  # "active" | "trial" | "cancelled"

@router.post("/sync-premium")
async def sync_premium_status(
    request: SyncPremiumRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Manually sync premium status from RevenueCat to Supabase
    Called by frontend after successful purchase
    
    Uses admin client to bypass RLS since this is a privileged operation.
    User authentication is still required via the current_user dependency.
    """
    try:
        # ✅ Use admin client to bypass RLS for the update
        # We still require authentication (current_user), but use service key for the update
        supabase = get_supabase_admin_client()
        
        print(f"🔄 Syncing premium for user: {current_user.uid}")
        print(f"   Email: {current_user.email}")
        print(f"   Plan: {request.subscription_plan}")
        print(f"   Status: {request.subscription_status}")
        
        # Update user in Supabase
        update_data = {
            'premium': True,
            'subscription_plan': request.subscription_plan,
            'subscription_status': request.subscription_status,
            'subscription_started_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('users').update(update_data).eq('uid', current_user.uid).execute()
        
        if not result.data or len(result.data) == 0:
            print(f"❌ No user found with uid: {current_user.uid}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        updated_user = result.data[0]
        print(f"✅ Premium synced successfully for {current_user.uid}")
        
        return {
            "message": "Premium status synced successfully",
            "user": updated_user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Sync premium error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync premium: {str(e)}"
        )

@router.get("/status")
async def get_subscription_status(
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get current subscription status from Supabase
    """
    try:
        # Use regular client for reads - user can read their own data
        supabase = get_supabase_client()
        
        result = supabase.table('users').select(
            'premium, subscription_plan, subscription_status, subscription_started_at, subscription_expires_at'
        ).eq('uid', current_user.uid).single().execute()
        
        return result.data
        
    except Exception as e:
        print(f"❌ Get subscription status error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get subscription status: {str(e)}"
        )


    """
    Get current subscription status from Supabase
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table('users').select(
            'premium, subscription_plan, subscription_status, subscription_started_at, subscription_expires_at'
        ).eq('uid', current_user.uid).single().execute()
        
        return result.data
        
    except Exception as e:
        print(f"❌ Get subscription status error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get subscription status: {str(e)}"
        )

@router.post("/sync-premium-test")
async def sync_premium_status_test(
    request: SyncPremiumRequest
):
    """
    TEST ENDPOINT - No authentication required
    ⚠️ USES SERVICE KEY - Remove this in production!
    """
    try:
        # ✅ Use admin client to bypass RLS
        supabase = get_supabase_admin_client()
        
        # Find all users to test with the first one
        users = supabase.table('users').select('*').limit(1).execute()
        
        if not users.data or len(users.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found in database"
            )
        
        test_user = users.data[0]
        test_uid = test_user['uid']
        
        print(f"🔄 [TEST] Syncing premium for user: {test_uid}")
        print(f"   Email: {test_user.get('email')}")
        print(f"   Plan: {request.subscription_plan}")
        print(f"   Status: {request.subscription_status}")
        
        update_data = {
            'premium': True,
            'subscription_plan': request.subscription_plan,
            'subscription_status': request.subscription_status,
            'subscription_started_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('users').update(update_data).eq('uid', test_uid).execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to update user"
            )
        
        updated_user = result.data[0]
        print(f"✅ [TEST] Premium synced successfully!")
        
        return {
            "message": "Premium status synced successfully (TEST MODE)",
            "user": updated_user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Sync premium error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync premium: {str(e)}"
        )
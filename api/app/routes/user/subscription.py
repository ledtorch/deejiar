# from fastapi import APIRouter, HTTPException, status, Depends

# from app.routes.user.auth import get_current_user
# from app.models.user import UserResponse
# from app.db.supabase import get_supabase_client

# router = APIRouter(prefix="/subscription", tags=["Subscription"])


# @router.get("/status")
# async def get_subscription_status(
#     current_user: UserResponse = Depends(get_current_user)
# ):
#     """
#     Get current subscription status
    
#     Subscription updates handled automatically via RevenueCat webhooks.
#     This endpoint provides read-only access to current status.
#     """
#     try:
#         supabase = get_supabase_client()
        
#         result = supabase.table('users').select(
#             'premium, subscription_plan, subscription_status, '
#             'subscription_started_at, subscription_expires_at'
#         ).eq('uid', current_user.uid).single().execute()
        
#         return result.data
        
#     except Exception as e:
#         print(f"❌ Get subscription status error: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to get subscription status: {str(e)}"
#         )
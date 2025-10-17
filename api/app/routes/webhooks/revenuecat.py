from fastapi import APIRouter, HTTPException, Request, Header
import os
from datetime import datetime
from app.db.supabase import get_supabase_admin_client

# router = APIRouter(tags=["Webhooks"])
router = APIRouter(prefix="/revenuecat")

@router.post("")
async def handle_revenuecat_webhook(
    request: Request,
    authorization: str = Header(None)
):
    """
    Handle RevenueCat webhook events and sync subscription data to Supabase
    
    RevenueCat sends Authorization header as: "Bearer <your_token>"
    This endpoint uses admin client to bypass RLS for webhook updates
    """
    
    # ─── Step 1: Verify Authorization ─────────────────────────────────
    expected_token = os.getenv('REVENUECAT_WEBHOOK_AUTH')
    
    if not expected_token:
        print("⚠️  REVENUECAT_WEBHOOK_AUTH not configured in environment")
        raise HTTPException(
            status_code=500, 
            detail="Webhook auth not configured"
        )
    
    if not authorization:
        print("❌ No authorization header provided")
        raise HTTPException(
            status_code=401, 
            detail="Missing authorization header"
        )
    
    # Extract token from "Bearer <token>" format
    auth_parts = authorization.split()
    if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
        print(f"❌ Invalid authorization format: {authorization}")
        raise HTTPException(
            status_code=401, 
            detail="Invalid authorization format. Expected: Bearer <token>"
        )
    
    received_token = auth_parts[1]
    
    if received_token != expected_token:
        print(f"❌ Token mismatch")
        print(f"   Expected: {expected_token[:10]}...")
        print(f"   Received: {received_token[:10]}...")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    print("✅ Authorization verified")

    # ─── Step 2: Parse Webhook Data ─────────────────────────────────
    try:
        data = await request.json()
        event_type = data.get('type')
        event = data.get('event', {})
        app_user_id = event.get('app_user_id')
        product_id = event.get('product_id')
        
        print(f"\n📨 Webhook received:")
        print(f"   Event Type: {event_type}")
        print(f"   User ID: {app_user_id}")
        print(f"   Product ID: {product_id}")
        
        if not app_user_id:
            print("⚠️  No app_user_id in webhook data")
            return {"status": "ignored", "reason": "missing_user_id"}
        
    except Exception as e:
        print(f"❌ Failed to parse webhook data: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid webhook data: {str(e)}"
        )

    # ─── Step 3: Update Supabase (Using Admin Client) ─────────────────
    try:
        # Use admin client to bypass RLS policies
        supabase = get_supabase_admin_client()
        
        # Handle different event types
        if event_type == 'INITIAL_PURCHASE':
            print(f"🎉 Processing initial purchase for {app_user_id}")
            
            update_data = {
                'premium': True,
                'subscription_plan': product_id,
                'subscription_status': 'active',
                'subscription_started_at': datetime.utcnow().isoformat()
            }
            
            result = supabase.table('users').update(update_data).eq('uid', app_user_id).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"⚠️  User not found: {app_user_id}")
                return {
                    "status": "warning", 
                    "message": f"User {app_user_id} not found in database"
                }
            
            print(f"✅ Updated {len(result.data)} user(s)")
            return {
                "status": "success", 
                "event": "initial_purchase",
                "user_id": app_user_id
            }
            
        elif event_type == 'RENEWAL':
            print(f"🔄 Processing renewal for {app_user_id}")
            
            update_data = {
                'premium': True,
                'subscription_status': 'active'
            }
            
            result = supabase.table('users').update(update_data).eq('uid', app_user_id).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"⚠️  User not found: {app_user_id}")
                return {
                    "status": "warning",
                    "message": f"User {app_user_id} not found in database"
                }
            
            print(f"✅ Updated {len(result.data)} user(s)")
            return {
                "status": "success",
                "event": "renewal",
                "user_id": app_user_id
            }
            
        elif event_type == 'CANCELLATION':
            print(f"❌ Processing cancellation for {app_user_id}")
            
            update_data = {
                'subscription_status': 'cancelled'
                # Note: Keep premium=True until expiration
            }
            
            result = supabase.table('users').update(update_data).eq('uid', app_user_id).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"⚠️  User not found: {app_user_id}")
                return {
                    "status": "warning",
                    "message": f"User {app_user_id} not found in database"
                }
            
            print(f"✅ Updated {len(result.data)} user(s)")
            return {
                "status": "success",
                "event": "cancellation",
                "user_id": app_user_id
            }
            
        elif event_type == 'EXPIRATION':
            print(f"⏰ Processing expiration for {app_user_id}")
            
            update_data = {
                'premium': False,
                'subscription_status': 'expired',
                'subscription_expires_at': datetime.utcnow().isoformat()
            }
            
            result = supabase.table('users').update(update_data).eq('uid', app_user_id).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"⚠️  User not found: {app_user_id}")
                return {
                    "status": "warning",
                    "message": f"User {app_user_id} not found in database"
                }
            
            print(f"✅ Updated {len(result.data)} user(s)")
            return {
                "status": "success",
                "event": "expiration",
                "user_id": app_user_id
            }
            
        elif event_type == 'TEST':
            print(f"🧪 Test webhook received")
            return {
                "status": "success",
                "message": "Test webhook received and processed"
            }
        
        else:
            print(f"⚠️  Unknown event type: {event_type}")
            return {
                "status": "ignored",
                "reason": "unknown_event_type",
                "event_type": event_type
            }
        
    except Exception as e:
        print(f"❌ Database update error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update database: {str(e)}"
        )
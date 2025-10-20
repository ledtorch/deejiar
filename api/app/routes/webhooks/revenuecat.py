from fastapi import APIRouter, HTTPException, Request, Header
import os
import json
from datetime import datetime
from app.db.supabase import get_supabase_admin_client

router = APIRouter(prefix="/revenuecat")

@router.post("")
async def handle_revenuecat_webhook(
    request: Request,
    authorization: str = Header(None)
):
    """
    Handle RevenueCat webhook events and sync subscription data to Supabase
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
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    print("✅ Authorization verified")

    # ─── Step 2: Parse Webhook Data ─────────────────────────────────
    try:
        data = await request.json()
        
        # 🔍 CRITICAL DEBUG: Log the ENTIRE payload structure
        print(f"\n🔍 ===== FULL WEBHOOK PAYLOAD =====")
        print(json.dumps(data, indent=2))
        print(f"===== END PAYLOAD =====\n")
        
        # Check all possible locations for event type
        event_type = None
        app_user_id = None
        product_id = None
        period_type = None
        purchased_at = None
        expiration_at = None
        
        # Try different payload structures
        if 'event' in data:
            event = data['event']
            print(f"🔍 Found 'event' object: {event}")
            event_type = event.get('type')
            app_user_id = event.get('app_user_id')
            product_id = event.get('product_id')
            period_type = event.get('period_type')
            purchased_at = event.get('purchased_at_ms')
            expiration_at = event.get('expiration_at_ms')
        
        # Fallback: check root level
        if not event_type:
            event_type = data.get('type')
            print(f"🔍 Checking root level 'type': {event_type}")
        
        if not app_user_id:
            app_user_id = data.get('app_user_id')
            print(f"🔍 Checking root level 'app_user_id': {app_user_id}")
        
        if not product_id:
            product_id = data.get('product_id')
            print(f"🔍 Checking root level 'product_id': {product_id}")
        
        # Log what we found
        print(f"\n📨 Parsed webhook data:")
        print(f"   Event Type: {event_type}")
        print(f"   User ID: {app_user_id}")
        print(f"   Product ID: {product_id}")
        print(f"   Period Type: {period_type}")
        print(f"   Purchased At: {purchased_at}")
        print(f"   Expiration At: {expiration_at}")
        
        if not app_user_id:
            print("⚠️  No app_user_id in webhook data")
            return {"status": "ignored", "reason": "missing_user_id"}
        
        if not event_type:
            print("⚠️  No event type in webhook data")
            print(f"🔍 Available keys in data: {list(data.keys())}")
            if 'event' in data:
                print(f"🔍 Available keys in event: {list(data['event'].keys())}")
            return {"status": "ignored", "reason": "missing_event_type", "debug": data}
        
    except Exception as e:
        print(f"❌ Failed to parse webhook data: {str(e)}")
        import traceback
        traceback.print_exc()
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
                'subscription_status': 'trial' if period_type == 'TRIAL' else 'active',
                'subscription_started_at': datetime.utcnow().isoformat()
            }
            
            # Add expiration if provided
            if expiration_at:
                expiration_date = datetime.fromtimestamp(expiration_at / 1000)
                update_data['subscription_expires_at'] = expiration_date.isoformat()
            
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
            
            # Update expiration date
            if expiration_at:
                expiration_date = datetime.fromtimestamp(expiration_at / 1000)
                update_data['subscription_expires_at'] = expiration_date.isoformat()
            
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
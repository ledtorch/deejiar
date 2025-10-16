from fastapi import APIRouter, HTTPException, Request, Header
import hmac
import hashlib
import os
from datetime import datetime
from app.db.supabase import get_supabase_client

router = APIRouter(tags=["Webhooks"])

@router.post("/revenuecat")
async def handle_revenuecat_webhook(
    request: Request,
    authorization: str = Header(None)
):
    # Verify authorization header  
    expected_auth = os.getenv('REVENUECAT_WEBHOOK_AUTH')
    if not authorization or authorization != expected_auth:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Parse webhook data
        body = await request.body()
        
        # Parse webhook data
        data = await request.json()
        event_type = data.get('type')
        app_user_id = data.get('event', {}).get('app_user_id')
        product_id = data.get('event', {}).get('product_id')
        
        supabase = get_supabase_client()
        
        # Handle different event types
        if event_type == 'INITIAL_PURCHASE':
            print(f"🎉 New purchase: {app_user_id} - {product_id}")
            result = supabase.table('users').update({
                'premium': True,
                'subscription_plan': product_id,
                'subscription_status': 'active',
                'subscription_started_at': datetime.utcnow().isoformat()
            }).eq('uid', app_user_id).execute()
            print(f"   Updated {len(result.data)} user(s)")
            
        elif event_type == 'RENEWAL':
            print(f"🔄 Renewal: {app_user_id}")
            result = supabase.table('users').update({
                'premium': True,
                'subscription_status': 'active'
            }).eq('uid', app_user_id).execute()
            print(f"   Updated {len(result.data)} user(s)")
            
        elif event_type == 'CANCELLATION':
            print(f"❌ Cancelled: {app_user_id}")
            result = supabase.table('users').update({
                'subscription_status': 'cancelled'
            }).eq('uid', app_user_id).execute()
            print(f"   Updated {len(result.data)} user(s)")
            
        elif event_type == 'EXPIRATION':
            print(f"⏰ Expired: {app_user_id}")
            result = supabase.table('users').update({
                'premium': False,
                'subscription_status': 'expired',
                'subscription_expires_at': datetime.utcnow().isoformat()
            }).eq('uid', app_user_id).execute()
            print(f"   Updated {len(result.data)} user(s)")
            
        elif event_type == 'TEST':
            print(f"🧪 Test webhook received")
            return {"status": "success", "message": "Test webhook received"}
        
        else:
            print(f"⚠️ Unknown event type: {event_type}")
            return {"status": "ignored", "reason": "unknown_event_type"}
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
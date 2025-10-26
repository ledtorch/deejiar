from datetime import datetime
import os
from app.db.supabase import get_supabase_admin_client

async def cleanup_deleted_accounts():
    """Permanently delete accounts after 30 days"""
    supabase = get_supabase_admin_client()
    now = datetime.utcnow().isoformat()
    
    result = supabase.table('users') \
        .select('uid, email') \
        .eq('account_status', 'pending_deletion') \
        .lte('deletion_scheduled_at', now) \
        .execute()
    
    if not result.data or len(result.data) == 0:
        print(f"[cleanup] No accounts to delete")
        return {"deleted_count": 0}
    
    deleted_accounts = []
    
    for user in result.data:
        print(f"[cleanup] Deleting: {user['email']} (UID: {user['uid']})")
        
        try:
            # Delete the user
            supabase.table('users').delete().eq('uid', user['uid']).execute()
            deleted_accounts.append(user)
            print(f"[cleanup] ✅ Deleted: {user['email']}")
            
        except Exception as e:
            print(f"[cleanup] ❌ Failed to delete {user['email']}: {str(e)}")
    
    # ✉️ Send email notification
    if deleted_accounts:
        try:
            import resend
            resend.api_key = os.getenv('RESEND_API_KEY')
            
            # Build simple text list
            account_list = "\n".join([
                f"UID: {acc['uid']}, Email: {acc['email']}"
                for acc in deleted_accounts
            ])
            
            resend.Emails.send({
                "from": "Deejiar System <system@deejiar.com>",
                "to": ["hi@deejiar.com"],
                "subject": f"Account Deletion - {len(deleted_accounts)} accounts deleted",
                "text": f"The following accounts were permanently deleted:\n\n{account_list}"
            })
            
            print(f"[cleanup] 📧 Sent email to hi@deejiar.com")
            
        except Exception as e:
            print(f"[cleanup] ⚠️ Failed to send email: {str(e)}")
    
    return {"deleted_count": len(deleted_accounts)}
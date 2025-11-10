import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Get the base directory (api folder)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables with correct path
env = os.getenv('ENV', 'development')
env_file = BASE_DIR / ('.env.production' if env == 'production' else '.env.local')

# Load the env file
load_dotenv(env_file)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# # 🐞 Print loaded values (remove in production!)
# print(f"SUPABASE_URL loaded: {SUPABASE_URL}")
# print(f"SUPABASE_ANON_KEY loaded: {SUPABASE_ANON_KEY[:20]}..." if SUPABASE_ANON_KEY else "SUPABASE_ANON_KEY not loaded")

# Validate that credentials are loaded
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError(
        f"Supabase credentials not found in {env_file}. "
        "Please ensure SUPABASE_URL and SUPABASE_ANON_KEY are set."
    )

# ─── JWT Auto-Refresh Configuration ────────────────────────────────────
# Refresh at 59 minutes to avoid edge cases to handle Supabase JWT expiration (1hour)
JWT_EXPIRY_SECONDS = 59 * 60

class SupabaseClientManager:
    """
    Manages Supabase client lifecycle to prevent JWT expiration.
    """
    
    def __init__(self):
        self._anon_client: Optional[Client] = None
        self._admin_client: Optional[Client] = None
        self._anon_created_at: Optional[datetime] = None
        self._admin_created_at: Optional[datetime] = None
    
    def _is_client_expired(self, created_at: Optional[datetime]) -> bool:
        """Check if client JWT is expired"""
        if not created_at:
            return True
        
        age = datetime.utcnow() - created_at
        return age.total_seconds() >= JWT_EXPIRY_SECONDS
    
    def get_anon_client(self) -> Client:
        """Get client, auto-refresh if expired"""
        if self._is_client_expired(self._anon_created_at):
            print("⚠️ Client expired. Recreating...")
            self._anon_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            self._anon_created_at = datetime.utcnow()
            print(f"✅ New client at {self._anon_created_at.isoformat()}")
        
        return self._anon_client
    
    def get_admin_client(self) -> Client:
        """Get admin client, auto-refresh if expired"""
        if not SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_SERVICE_KEY not found")
        
        if self._is_client_expired(self._admin_created_at):
            print("⚠️ Admin client expired. Recreating...")
            self._admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            self._admin_created_at = datetime.utcnow()
            print(f"✅ New admin client at {self._admin_created_at.isoformat()}")
        
        return self._admin_client
    
    def force_refresh_anon_client(self) -> Client:
        """Force recreation of client"""
        print("🔄 Force refreshing client...")
        self._anon_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self._anon_created_at = datetime.utcnow()
        return self._anon_client

# ✅ Global singleton manager
_client_manager = SupabaseClientManager()

# ✅ Public API (same function names, different implementation)
def get_supabase_client() -> Client:
    """Get client with auto-refresh"""
    return _client_manager.get_anon_client()

def get_supabase_admin_client() -> Client:
    """Get admin client with auto-refresh"""
    return _client_manager.get_admin_client()

def force_refresh_clients():
    """Force refresh both clients"""
    _client_manager.force_refresh_anon_client()
    _client_manager.force_refresh_admin_client()

# # Create Supabase clients
# def get_supabase_client() -> Client:
#     """Get regular Supabase client for user operations"""
#     return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# def get_supabase_admin_client() -> Client:
#     """Get admin Supabase client for privileged operations"""
#     if not SUPABASE_SERVICE_KEY:
#         raise ValueError("SUPABASE_SERVICE_KEY not found for admin operations")
#     return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
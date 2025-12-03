import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

from supabase.lib.client_options import ClientOptions

# Get the base directory (api folder)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
env = os.getenv('ENV', 'development')
env_file = BASE_DIR / ('.env.production' if env == 'production' else '.env.local')
load_dotenv(env_file)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY") # 🧪 Testing: Use New API key

# Validate that all credentials are loaded
missing = []
if not SUPABASE_URL:
    missing.append("SUPABASE_URL")
if not SUPABASE_ANON_KEY:
    missing.append("SUPABASE_ANON_KEY")
if not SUPABASE_SERVICE_KEY:
    missing.append("SUPABASE_SERVICE_KEY")
# 🧪 Testing: Use New API key
if not SUPABASE_SECRET_KEY:
    missing.append("SUPABASE_SECRET_KEY")

if missing:
    raise ValueError(
        f"Missing Supabase credentials in {env_file}: {', '.join(missing)}\n"
        f"Loaded from: {env_file}\n"
        f"Current ENV: {env}"
    )

# 🐞 Print loaded values
print(f"SUPABASE_URL loaded: {SUPABASE_URL}")
print(f"SUPABASE_ANON_KEY loaded: {SUPABASE_ANON_KEY[:10]}...{SUPABASE_ANON_KEY[-10:]}" if SUPABASE_ANON_KEY else "SUPABASE_ANON_KEY not loaded")
print(f"SUPABASE_SERVICE_KEY loaded: {SUPABASE_SERVICE_KEY[:10]}...{SUPABASE_SERVICE_KEY[-10:]}" if SUPABASE_SERVICE_KEY else "SUPABASE_SERVICE_KEY not loaded")
# 🧪 Testing: Use New API key
print(f"SUPABASE_SECRET_KEY loaded: {SUPABASE_SECRET_KEY[:10]}...{SUPABASE_SECRET_KEY[-10:]}" if SUPABASE_SECRET_KEY else "SUPABASE_SECRET_KEY not loaded")

# ─── Client Management ──────────────────────────────────────────────────
# Recreate client objects every 50 minutes to prevent stale HTTP connections 
# (Supabase access token expires in 1 hour)
CLIENT_REFRESH_SECONDS = 50 * 60

# Disable Supabase auto-refresh
client_options = ClientOptions(
    auto_refresh_token=False,
    persist_session=False
)

class SupabaseClientManager:
    def __init__(self):
        self._anon_client: Optional[Client] = None
        self._admin_client: Optional[Client] = None
        self._anon_created_at: Optional[datetime] = None
        self._admin_created_at: Optional[datetime] = None
        
        # 🧪 Testing: Use New API key
        self._newapi_admin_client: Optional[Client] = None
        self._newapi_admin_created_at: Optional[datetime] = None
    
    # Check if client JWT is expired
    def _is_client_expired(self, created_at: Optional[datetime]) -> bool:
        # None timestamp = client not yet created (triggers lazy initialization)
        if not created_at:
            return True
        
        age = datetime.utcnow() - created_at
        return age.total_seconds() >= CLIENT_REFRESH_SECONDS
    
    # Create anon client
    def get_anon_client(self) -> Client:
        if self._is_client_expired(self._anon_created_at):
            print("⚠️ Client expired. Recreating...")
            self._anon_client = create_client(
                SUPABASE_URL, 
                SUPABASE_ANON_KEY,
                options=client_options
            )
            self._anon_created_at = datetime.utcnow()
            print(f"✅ New client at {self._anon_created_at.isoformat()}")
        
        return self._anon_client
    
    # Create admin client
    def get_admin_client(self) -> Client:
        if self._is_client_expired(self._admin_created_at):
            print("⚠️ Admin client expired. Recreating...")
            self._admin_client = create_client(
                SUPABASE_URL, 
                SUPABASE_SERVICE_KEY,
                options=client_options
            )
            self._admin_created_at = datetime.utcnow()
            print(f"✅ New admin client at {self._admin_created_at.isoformat()}")
        
        return self._admin_client
    
    # 🧪 Testing: Use New API key
    # Create admin client with new secret key (for auth.admin operations)
    def get_newapi_admin_client(self) -> Client:
        if not SUPABASE_SECRET_KEY:
            print("⚠️ SUPABASE_SECRET_KEY not set, falling back to legacy SERVICE_KEY")
            return self.get_admin_client()
        
        if self._is_client_expired(self._newapi_admin_created_at):
            print("⚠️ Admin client (new key) expired. Recreating...")
            self._newapi_admin_client = create_client(
                SUPABASE_URL, 
                SUPABASE_SECRET_KEY,
                options=client_options
            )
            self._newapi_admin_created_at = datetime.utcnow()
            print(f"✅ New admin client (new key) at {self._newapi_admin_created_at.isoformat()}")
        
        return self._newapi_admin_client


    def force_refresh_anon_client(self) -> Client:
        """Force recreation of client"""
        print("🔄 Force refreshing client...")
        self._anon_client = create_client(
            SUPABASE_URL, 
            SUPABASE_ANON_KEY,
            options=client_options  # ← FIX: Pass options here!
        )
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

# 🧪 Testing: Use New API key
def get_newapi_admin_client() -> Client:
    """Get admin client with auto-refresh"""
    return _client_manager.get_newapi_admin_client()

def force_refresh_clients():
    """Force refresh both clients"""
    _client_manager.force_refresh_anon_client()
    _client_manager.force_refresh_admin_client()

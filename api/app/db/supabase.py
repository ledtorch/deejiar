# app/db/supabase.py
import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Get the base directory (api folder)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Goes up to api/

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

# Create Supabase clients
def get_supabase_client() -> Client:
    """Get regular Supabase client for user operations"""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_admin_client() -> Client:
    """Get admin Supabase client for privileged operations"""
    if not SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_SERVICE_KEY not found for admin operations")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
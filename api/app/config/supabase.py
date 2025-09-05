import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
env_file = '../.env.production' if os.getenv('ENV') == 'production' else '../.env.local'
load_dotenv(env_file)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # For admin operations

# Create Supabase clients
def get_supabase_client() -> Client:
    """Get regular Supabase client for user operations"""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_admin_client() -> Client:
    """Get admin Supabase client for privileged operations"""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
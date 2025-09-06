from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
security = HTTPBasic()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify admin credentials"""
    correct_username = secrets.compare_digest(
        credentials.username, ADMIN_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, ADMIN_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.post("/login")
async def admin_login(request: Request):
    """Admin login endpoint"""
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )
    
    return {
        "message": "Admin login successful",
        "role": "admin"
    }

@router.get("/verify")
async def verify_admin_status(admin: str = Depends(verify_admin)):
    """Verify admin is logged in"""
    return {"admin": admin, "verified": True}
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import secrets
from dotenv import load_dotenv
from ..editor import list_json_files, get_json_data, save_json_data

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Admin Authentication"])
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
        "role": "admin",
        "username": username
    }

@router.get("/verify")
async def verify_admin_status(admin: str = Depends(verify_admin)):
    """Verify admin is logged in"""
    return {"admin": admin, "verified": True}

@router.post("/logout")
async def admin_logout():
    """Admin logout endpoint"""
    return {"message": "Admin logout successful"}

# # ─── Protected Dashboard API Routes ──────────────────────────────────

# @router.get("/json-files")
# async def get_json_files(admin: str = Depends(verify_admin)):
#     """Get list of JSON files - Admin only"""
#     return list_json_files()

# @router.get("/json-data/{filename}")
# async def get_json_data_endpoint(filename: str, admin: str = Depends(verify_admin)):
#     """Get JSON file data - Admin only"""
#     try:
#         return get_json_data(filename)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/save/{filename}")
# async def save_json_endpoint(filename: str, request: Request, admin: str = Depends(verify_admin)):
#     """Save JSON file data - Admin only"""
#     try:
#         data = await request.json()
#         new_filename = save_json_data(filename, data)
#         return {
#             "message": "JSON file updated successfully",
#             "filename": new_filename
#         }
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
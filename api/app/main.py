import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
# Environment
from dotenv import load_dotenv
# Modules
from app.routes.user.auth import router as user_auth_router
from app.routes.admin.auth import router as admin_auth_router
from app.routes.map import get_map_json
from app.routes.search import router as search_router
from app.routes.search import search_stores as perform_search_stores
from app.routes.editor import list_json_files, get_json_data, save_json_data

from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pathlib import Path

# ─── Initialize FastAPI ────────────────────────────────
app = FastAPI(debug=True)

# Mount static assets for CDN-like access
app.mount(
    "/cdn",
    StaticFiles(directory=Path(__file__).parent.parent / "assets"),
    name="cdn"
)

# Load environment settings
env_file = '../.env.production' if os.getenv('ENV') == 'production' else '../.env.local'
load_dotenv(env_file)
print(f"ENV file URL: {env_file}")

# CORS config
env = os.getenv('ENV', 'development')
if env == 'development':
        origins = [
            "https://localhost:5174",  # iOS Map app
            "https://192.168.50.85:5174",  # iOS Map app
            "https://localhost:5173",  # Dashboard app
            "capacitor://localhost"
    ]
else:
    origins = ["https://deejiar.com", "https://app.deejiar.com", "https://qa.deejiar.com", "capacitor://localhost", "deejiar://app.deejiar.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ────────────────────────────────────
app.include_router(user_auth_router, prefix="/api/user")
app.include_router(admin_auth_router, prefix="/api/admin")
app.include_router(search_router, prefix="/api/search", tags=["search"])

# ─── Pages ────────────────────────────────────────────
@app.get("/")
async def root():
    return {"FastAPI is running"}

@app.get("/dashboard")
async def dashboard():
    return {"message": "Login successful"}

# ─── App API ────────────────────────────────────
@app.get("/map/{filename}")
async def serve_map_data(filename: str):
    try:
        return get_map_json(filename)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_stores(
    q: str = Query(None, description="Search query"),
    type: str = Query(None, description="Filter by type"),
    tags: list[str] = Query(default=[], description="Filter by tags")
):
    return await perform_search_stores(q, type, tags)

# ─── TEMPORARY UNPROTECTED ROUTES (REMOVE AFTER TESTING) ─────────────────────
@app.get("/api/admin/auth/json-files")
async def temp_get_json_files():
    return list_json_files()

@app.get("/api/admin/auth/json-data/{filename}")
async def temp_get_json_data(filename: str):
    try:
        return get_json_data(filename)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/auth/save/{filename}")
async def temp_save_json_data(filename: str, request: Request):
    try:
        data = await request.json()
        new_filename = save_json_data(filename, data)
        return {
            "message": "JSON file updated successfully",
            "filename": new_filename
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
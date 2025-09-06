import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
# Environment
from dotenv import load_dotenv
# Modules
from app.routes.user import auth as user_auth
from app.routes.admin import auth as admin_auth
from app.routes.map import get_map_json
from app.routes.editor import list_json_files, get_json_data, save_json_data

from fastapi.staticfiles import StaticFiles
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
    origins = ["https://deejiar.com", "https://qa.deejiar.com", "capacitor://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pages
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

# ─── Dashboard API ────────────────────────────────────
# Authentication
# User account details
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

@app.post("/login")
async def login(request: Request):
    form = await request.json()
    username = form.get("username")
    password = form.get("password")
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "message": "Login successful",
        "redirect": "/dashboard"
    }

@app.get("/json-files")
async def get_json_files():
    return list_json_files()

@app.get("/json-data/{filename}")
async def get_json_data_endpoint(filename: str):
    try:
        return get_json_data(filename)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save/{filename}")
async def save_json_endpoint(filename: str, request: Request):
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
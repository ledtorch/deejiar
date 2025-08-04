import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
# Environment
from dotenv import load_dotenv
# Modules
from routes.editor import list_json_files, flatten_features, save_reconstructed_features

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

# User account details
USER_ACCOUNT = {
    "username": "jerry",
    "password": "0000"
}

# Load environment settings
env_file = '../.env.production' if os.getenv('ENV') == 'production' else '../.env.local'
load_dotenv(env_file)
print(f"ENV file URL: {env_file}")

# CORS config
env = os.getenv('ENV', 'development')
if env == 'development':
    origins = ["http://localhost:5173"]
else:
    origins = ["https://deejiar.com/api"]

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


# ─── Test Google API ────────────────────────────────────
# GOOGLE_API_KEY = os.getenv("GOOGLE_NEWPLACE_API_KEY")  # or just hardcode for test

# def fix_mojibake(s):
#     try:
#         return s.encode('latin1').decode('utf8')
#     except Exception:
#         return s

# @app.get("/test_GoogleAPI")
# async def test_GoogleAPI(place_id: str = Query(...)):
#     url = "https://places.googleapis.com/v1/places/" + place_id
#     headers = {
#         "X-Goog-Api-Key": GOOGLE_API_KEY,
#         "X-Goog-FieldMask": "id,displayName,formattedAddress,location,photos,websiteUri,rating,userRatingCount"
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         data = response.json()

#     # Recursively fix all strings in the response
#     def recursive_fix(obj):
#         if isinstance(obj, dict):
#             return {k: recursive_fix(v) for k, v in obj.items()}
#         elif isinstance(obj, list):
#             return [recursive_fix(i) for i in obj]
#         elif isinstance(obj, str):
#             return fix_mojibake(obj)
#         else:
#             return obj

#     data = recursive_fix(data)
#     return data

# Authentication
@app.post("/login")
async def login(request: Request):
    form = await request.json()
    username = form.get("username")
    password = form.get("password")
    if username != USER_ACCOUNT["username"] or password != USER_ACCOUNT["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "message": "Login successful",
        "redirect": "/dashboard"
    }

# Editor
@app.get("/json-files")
async def get_json_files():
    return list_json_files()

@app.get("/json-data/{filename}")
async def get_features(filename: str):
    try:
        return flatten_features(filename)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save/{filename}")
async def reconstruct_features(filename: str, request: Request):
    try:
        features = await request.json()
        new_filename = save_reconstructed_features(filename, features)
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
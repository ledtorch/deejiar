import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from editor import list_json_files, flatten_features, reconstruct_json
import json
from pathlib import Path
from datetime import datetime

# Load environment settings
env_file = '../.env.production' if os.getenv('FASTAPI_ENV') == 'production' else '../.env.local'
load_dotenv(env_file)
print(f"ENV file URL: {env_file}")

# Define JSON_PATH relative to this file
JSON_PATH = Path(__file__).parent.parent / 'data'

# User account details
USER_ACCOUNT = {
    "username": "jerry",
    "password": "0000"
}

app = FastAPI()

# Enable CORS
if os.getenv('ENV') == 'development':
    origins = [
        "http://localhost",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
else:
    origins = [
        "https://deejiar.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(request: Request):
    form = await request.json()
    username = form.get("account")
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

@app.get("/")
async def root():
    return {"FastAPI is running"}

@app.get("/dashboard")
async def dashboard():
    return {"message": "Login successful"}

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
    json_file_path = os.path.join(JSON_PATH, f"{filename}.json")

    # Make a backup of the current JSON file
    if os.path.exists(json_file_path):
        timestamp = datetime.now().strftime('%H%M%S')
        backup_path = json_file_path.replace('.json', f'_backup_{timestamp}.json')
        os.rename(json_file_path, backup_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        features = await request.json()
        result = reconstruct_json(features)
        
        # Save the reconstructed JSON to a file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        return {"message": f"{filename}.json updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with "python app.py" with full uvicorn features
# Below could be removed if running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)
import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from editor import list_json_files, flatten_features, save_reconstructed_features

# Load environment settings
env_file = '../.env.production' if os.getenv('FASTAPI_ENV') == 'production' else '../.env.local'
load_dotenv(env_file)
print(f"ENV file URL: {env_file}")

# User account details
USER_ACCOUNT = {
    "username": "jerry",
    "password": "0000"
}

app = FastAPI()

# Enable CORS
if os.getenv('ENV') == 'development':
    origins = [
        "http://localhost:5173"
    ]
else:
    origins = [
        "https://deejiar.com/api"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"FastAPI is running"}

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

# Run with "python app.py" with full uvicorn features
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)
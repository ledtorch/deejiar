import os
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment settings
env_file = '.env.production' if os.getenv('FASTAPI_ENV') == 'production' else '.env.local'
print(f"Loading environment variables from: {env_file}")
load_dotenv(env_file)

# Environment variables
DATACENTER_API_BASE_URL = os.getenv('DATACENTER_API_BASE_URL', 'http://127.0.0.1:5000')

# User account details
USER_ACCOUNT = {
    "username": "jerry",
    "password": "0000"
}

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
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

@app.get("/dashboard")
async def dashboard():
    return {"message": "Login successful"}

@app.get("/")
async def root():
    return {"FastAPI"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
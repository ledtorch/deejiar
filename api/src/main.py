# src/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from dotenv import load_dotenv

# Load environment variables
env_file = '.env.production' if os.getenv('FASTAPI_ENV') == 'production' else '.env.local'
load_dotenv(env_file)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT settings
class Settings:
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')

@AuthJWT.load_config
def get_config():
    return Settings()

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import os
from datetime import datetime, timedelta
from typing import List
import uvicorn

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from og import og_router

from dotenv import load_dotenv

from editor import list_json_files, flatten_features, reconstruct_json

# Load environment variables
env_file = '.env.production' if os.getenv('FASTAPI_ENV') == 'production' else '.env.local'
load_dotenv(env_file)

# Constants
STORES_JSON_PATH = '../data/'
DATACENTER_API_BASE_URL = os.getenv('DATACENTER_API_BASE_URL')
SECRET_KEY = os.getenv("SECRET_KEY", "your_jwt_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock user database
users = {
    "jerry": {
        "username": "jerry",
        "hashed_password": pwd_context.hash("0000")
    }
}

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = User(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.get("/")
async def root():
    return {"message": "FastAPI Server"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/json-files", response_model=List[str])
async def get_json_files():
    return list_json_files()

@app.get("/json-data/{filename}")
async def get_json_data(filename: str):
    try:
        simplified_data = flatten_features(filename)
        return simplified_data
    except HTTPException as e:
        raise e

@app.post("/save/{filename}")
async def update_json(filename: str, request: Request):
    json_file_path = os.path.join(STORES_JSON_PATH, f"{filename}.json")

    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Backup current file
    timestamp = datetime.now().strftime('%H%M%S')
    backup_path = json_file_path.replace('.json', f'_backup_{timestamp}.json')
    os.rename(json_file_path, backup_path)

    edited_data = await request.json()

    try:
        reconstructed_data = reconstruct_json(edited_data)
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(reconstructed_data, f, ensure_ascii=False, indent=4)
    except HTTPException as e:
        raise e

    return {"message": f"{filename} updated successfully"}

# Add this line after creating the FastAPI app
app.include_router(og_router, prefix="/og")

# Add this line after creating the FastAPI app
templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
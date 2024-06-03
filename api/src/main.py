# Standard libraries
import os
import json
from datetime import timedelta, datetime

# Environment settings
from dotenv import load_dotenv

# FastAPI framework
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# Local modules
from . import json_utils
# from .og import og_router

# Load environment variables
env_file = '.env.production' if os.getenv('FASTAPI_ENV') == 'production' else '.env.local'
load_dotenv(env_file)

# JWT settings
SECRET_KEY = "your_jwt_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Files and sources
STORES_JSON_PATH = '../data/'

# User account
users_db = {
    "jerry": {"username": "jerry", "password": "$2b$12$4u8elZ5wA/Rf5FVb/1R4AeNi.cV.dE16ndPeU/gj3AG/82Zg/aD5e"}  # Hashed password for "0000"
}

# FastAPI app config
app = FastAPI()

# Enable CORS for all routes and origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the blueprint for OG image feature
# app.include_router(og_router)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
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
        status_code=HTTPException.status_code,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# 🐞 Debug URL, check deejiar.com/admin/api
@app.get("/")
async def home():
    print("Home route accessed")
    return {"message": "FastAPI Server"}

# Account
@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTPException.status_code,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dashboard
@app.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    return {"logged_in_as": current_user["username"]}

# JSON
@app.get("/json-files", response_model=list)
async def get_json_files():
    return json_utils.list_json_files()

@app.get("/json-data/{filename}", response_model=dict)
async def get_json_data(filename: str):
    simplified_data = json_utils.flatten_features(f'{filename}.json')
    if simplified_data is not None:
        return simplified_data
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.post("/save/{filename}", response_model=dict)
async def update_json(filename: str, request: Request):
    base_directory = '../data/'
    json_file_path = os.path.join(base_directory, f"{filename}.json")

    # Make a backup of the current JSON file
    if os.path.exists(json_file_path):
        timestamp = datetime.now().strftime('%H%M%S')
        backup_path = json_file_path.replace('.json', f'_backup_{timestamp}.json')
        os.rename(json_file_path, backup_path)
    else:
        # If the file does not exist, do not proceed
        raise HTTPException(status_code=404, detail="File not found")

    # Get the edited data from the request
    edited_data = await request.json()

    try:
        # Use the reconstruct_json function to rebuild the JSON structure
        reconstructed_data = json_utils.reconstruct_json(edited_data)

        # Save the new JSON data
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(reconstructed_data, f, ensure_ascii=False, indent=4)

    except ValueError as e:
        # Handle the error by returning an error response
        raise HTTPException(status_code=400, detail=str(e))  # Bad request due to data error

    # If everything went well
    return {"message": f"{filename} updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

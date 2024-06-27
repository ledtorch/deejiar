from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from src.auth.schemas import UserLogin
from src.auth.models import User

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/login")
async def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    user_data = User.get_user(user.username)  # Assuming a method to get user data
    if not user_data or not pwd_context.verify(user.password, user_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/dashboard")
async def dashboard(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"logged_in_as": current_user}
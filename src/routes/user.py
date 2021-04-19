from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.users import Token, User, UserSignup
from src.handlers.users import (
    authenticate_user, create_access_token, get_current_active_user,
    UserManager
)



router = APIRouter()


@router.post("/signup/")
async def signup(signup: UserSignup):
    user = UserManager()
    user_data = User(**signup.dict())
    u = user.create_user(user_data)
    if u:
        return signup
    else:
        return {"message": "failed"}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def profile(current_user: User = Depends(get_current_active_user)):
    return current_user


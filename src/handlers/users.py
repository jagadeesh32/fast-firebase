from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config import db, SECRET_KEY, ALGORITHM
from src.models.users import User, TokenData


class UserManager:
    def __init__(self):
        self.db = db
        self.collction = "users"
        
    def create_user(self, model):
        doc = db.collection(self.collction).document(str(model.email)).get()
        if doc.exists:
            print("Duplicate Key Found. {}".format(doc.get('email')))
            return False
        
        doc = self.db.collection(self.collction).document(str(model.email)).set(model.dict())
        if not doc:
            raise("document not saved")
        return True
    
    def get_user(self, document):
        doc = db.collection(self.collction).document(document).get()
        if doc.exists:
            print("Duplicate Key Found. {}".format(doc.get('email')))
            return doc.to_dict()
        else:
            return None
    
    def update_user(self, document, data={}):
        print(data)
        doc_ref = db.collection(self.collction).document(document).update(data)
        if not doc_ref:
            raise("document not saved")
        return True
    
    def delete_user(self, document):
        doc_ref = db.collection(self.collction).document(document).delete()
        return True
    
    def get_all_users(self):
        docs = db.collection(self.collction).stream()
        users_list = [doc.to_dict() for doc in docs ]
        return users_list
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(email: str):
    u = UserManager()
    user = u.get_user(email)
    if user is not None:
        return User(**user)


def authenticate_user(email: str, password: str):
    user = get_user(email=email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
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
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


import uuid
import json
from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel
from pydantic.networks import AnyUrl, HttpUrl
from pydantic.types import T, UUID4, constr
from pydantic.typing import NONE_TYPES


class Profile(BaseModel):
    website: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    github: Optional[str] = None


class User(BaseModel):
    username: Optional[str] = ""
    email: constr(strip_whitespace=True, min_length=1, max_length=100)
    password: constr(min_length=8, max_length=255)
    first_name: Optional[constr(max_length=50)] = None
    last_name: Optional[constr(max_length=50)] = None
    created_at: Optional[datetime] = datetime.now()
    dob: Optional[datetime] = datetime.now()
    is_active: Optional[bool] = True
    profile = Profile()

    def __str__(self):
        return str(self.email)
    
    def get_schema(self):
        print(self.schema_json(indent=2))
        return True
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserSignup(BaseModel):
    email: constr(strip_whitespace=True, min_length=1, max_length=100)
    password: constr(min_length=8, max_length=255)

class UserSignin(BaseModel):
    email: constr(strip_whitespace=True, min_length=1, max_length=100)
    password: constr(min_length=8, max_length=255)
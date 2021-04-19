import uuid
import json
from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel
from pydantic.types import UUID4, constr


class Blog(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=100)
    slug: constr(strip_whitespace=True, min_length=1, max_length=150)
    
    meta_keywords: Optional[List] = []
    meta_description: constr(min_length=8, max_length=255)
    description: Optional[str] = None
    status: Optional[bool] = True
    tags: Optional[List] = []
    author: Optional[str] = ''
    
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    
    def __str__(self):
        return str(self.slug)            
    
    def get_schema(self):
        print(self.schema_json(indent=2))
        return True


class CreateArticle(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=100)
    meta_keywords: Optional[List] = []
    meta_description: constr(min_length=8, max_length=255)
    description: Optional[str] = None
    tags: Optional[List] = []

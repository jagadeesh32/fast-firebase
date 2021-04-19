from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from slugify import slugify

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.blog import Blog, CreateArticle
from src.models.users import User
from src.handlers.users import get_current_active_user
from src.handlers.blogs import BlogManager

router = APIRouter()


@router.get("/article/")
async def create_article(current_user: User = Depends(get_current_active_user)):
    
    b = BlogManager()
    status = b.get_all_articles()
    if status:
        return status
    else:
        return {"message": "failed"}
    

@router.post("/article/")
async def create_article(article: CreateArticle, current_user: User = Depends(get_current_active_user)):
    print(article.dict())
    
    data = article.dict()
    data["slug"] = slugify(data["title"])
    data["author"] = current_user.email
    
    b = BlogManager()
    article_data = Blog(**data)
    status = b.create_article(article_data)
    if status:
        return b.get_article(document=article_data.slug)
    else:
        return {"message": "failed"}


@router.put("/article/")
async def update_article(article: Blog, current_user: User = Depends(get_current_active_user)):
    
    data = article.dict()

    b = BlogManager()
    article_data = Blog(**data)
    #article_data = article_data.dict()
    #print(article_data)
    status = b.update_article(document=article_data.slug, model=article_data)
    
    if status:
        return b.get_article(document=article_data.slug)
    else:
        return {"message": "failed"}


@router.get("/article/{slug}")
async def get_article(slug, current_user: User = Depends(get_current_active_user)):
    b = BlogManager()
    status = b.get_article(document=slug)
    if status:
        return status
    else:
        return {"message": "failed"}


import os
from pathlib import Path
import firebase_admin
from firebase_admin import firestore
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


config = load_dotenv(os.path.join(BASE_DIR, ".env"))

firebase_admin.initialize_app()
db = firestore.client()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300   # In 5 Hours


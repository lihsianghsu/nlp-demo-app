# env.py
import os

PUBLIC_MODE = os.getenv("LS_PUBLIC", "true").lower() == "true"
ADMIN_EMAILS = os.getenv("LS_ADMIN_EMAILS", "").split(",") if not PUBLIC_MODE else []
SECRET_KEY = os.getenv("LS_SECRET_KEY", "default_secret_key")
DATABASE_URL = os.getenv("LS_DATABASE_URL", "sqlite:///./local.db") 
API_BASE_URL = os.getenv("LS_API_BASE_URL", "http://localhost:8000")    
REDIS_URL = os.getenv("LS_REDIS_URL", "redis://localhost:6379/0")

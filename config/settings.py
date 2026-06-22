import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
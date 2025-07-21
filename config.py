import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present (dev only)
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///db.sqlite3"
    )


from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # 2Captcha
    CAPTCHA_API_KEY: str = os.getenv("CAPTCHA_API_KEY", "")
    CAPTCHA_TIMEOUT: int = 180

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./maha_verify.db")

    # Session
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development-secret-key-change-in-production")
    SESSION_TIMEOUT: int = 3600  # 1 hour

    # Server
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 200 * 1024 * 1024  # 200MB

    # RERA Portal
    RERA_PORTAL_URL: str = "https://maharera.mahaonline.gov.in"
    RERA_PORTAL_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        super().__init__(**data)
        # Create upload directory if it doesn't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

# Create global settings instance
settings = Settings()

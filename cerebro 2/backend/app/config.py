"""Configuration settings for Cerebro application."""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Config
    app_name: str = "Cerebro"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Auth0 Configuration
    auth0_domain: Optional[str] = os.getenv("AUTH0_DOMAIN")
    auth0_client_id: Optional[str] = os.getenv("AUTH0_CLIENT_ID")
    auth0_client_secret: Optional[str] = os.getenv("AUTH0_CLIENT_SECRET")
    auth0_audience: Optional[str] = os.getenv("AUTH0_AUDIENCE")
    
    # API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    job_api_key: Optional[str] = os.getenv("JOB_API_KEY")
    freepik_api_key: Optional[str] = os.getenv("FREEPIK_API_KEY")
    
    # Gmail API (OAuth credentials - JSON file paths)
    gmail_credentials_path: Optional[str] = os.getenv("GMAIL_CREDENTIALS_PATH")
    gmail_token_path: Optional[str] = os.getenv("GMAIL_TOKEN_PATH")
    
    # Data Storage
    data_dir: str = os.getenv("DATA_DIR", "data/user_states")
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:3003",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


settings = Settings()

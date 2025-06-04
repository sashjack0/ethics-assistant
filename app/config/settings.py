"""
Configuration settings for the Ethics Assistant application.
"""
import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Environment(str, Enum):
    """Environment types."""
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """Application settings."""
    # Environment
    ENV: Environment = Environment.LOCAL
    
    # API Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 500
    OPENAI_TEMPERATURE: float = 0.5
    
    # Application Configuration
    APP_NAME: str = "AI Ethics & Fairness Review Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[Path] = None
    
    # Rate Limiting
    RATE_LIMIT_SECONDS: int = 5
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    """
    Get application settings based on environment.
    
    Returns:
        Settings: Application settings instance
    """
    env = os.getenv("ENV", "local").lower()
    env_file = f".env.{env}" if env != "local" else ".env"
    
    if Path(env_file).exists():
        load_dotenv(env_file)
    
    return Settings()

# Create global settings instance
settings = get_settings() 
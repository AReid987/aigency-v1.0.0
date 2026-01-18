from pydantic import BaseSettings, validator
from typing import List, Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Multi-Source Dashboard"
    
    # Database
    DATABASE_URL: str
    DATABASE_TEST_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_URL: str = "redis://localhost:6379/1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # External APIs - Reddit
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: str = "DashboardApp/1.0.0"
    
    # External APIs - News
    GNEWS_API_KEY: Optional[str] = None
    NEWSAPI_KEY: Optional[str] = None
    
    # Publishing APIs
    DEVTO_API_KEY: Optional[str] = None
    WORDPRESS_USERNAME: Optional[str] = None
    WORDPRESS_PASSWORD: Optional[str] = None
    WORDPRESS_SITE_URL: Optional[str] = None
    
    GHOST_ADMIN_API_KEY: Optional[str] = None
    GHOST_API_URL: Optional[str] = None
    GHOST_CONTENT_API_KEY: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Rate Limiting
    HACKER_NEWS_RATE_LIMIT: int = 60  # requests per minute
    REDDIT_RATE_LIMIT: int = 100  # requests per minute
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
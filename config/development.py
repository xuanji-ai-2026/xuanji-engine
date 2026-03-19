"""
Development Configuration
"""
import os
from typing import List
from .production import ProductionConfig

class DevelopmentConfig(ProductionConfig):
    """Development environment configuration"""
    
    # Application
    APP_ENVIRONMENT: str = 'development'
    DEBUG: bool = True
    
    # API
    API_PORT: int = 8000  # Different from production
    API_WORKERS: int = 1  # Single worker for development
    
    # DeepSeek
    DEEPSEEK_TIMEOUT: int = 60  # Longer timeout for development
    
    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_NAME: str = os.getenv('DB_NAME', 'xuanji_engine_dev')
    DB_POOL_SIZE: int = 5  # Smaller pool for development
    
    # Redis
    REDIS_DB: int = 1  # Separate database for development
    REDIS_POOL_SIZE: int = 5  # Smaller pool for development
    
    # Logging
    LOG_LEVEL: str = 'DEBUG'  # Debug level for development
    LOG_FORMAT: str = 'text'  # Human-readable format
    LOG_OUTPUT: str = 'stdout'
    LOG_FILE: str = 'app.log'  # Local file
    
    # Monitoring
    METRICS_ENABLED: bool = False  # Disable metrics in development
    
    # Performance
    PERFORMANCE_MAX_CONCURRENT_REQUESTS: int = 100  # Lower for development
    PERFORMANCE_REQUEST_TIMEOUT: int = 120  # Longer for debugging
    
    # Security
    SECRET_KEY: str = 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY: str = 'dev-jwt-secret-key-change-in-production'
    JWT_EXPIRATION_HOURS: int = 168  # 7 days for development
    CORS_ORIGINS: List[str] = ['http://localhost:3000', 'http://localhost:8000']
    RATE_LIMIT_ENABLED: bool = False  # Disable rate limit in development
    
    # Development-specific
    HOT_RELOAD: bool = True
    AUTO_RELOAD: bool = True
    DEBUG_TOOLBAR: bool = True
    SQL_ECHO: bool = True  # Log SQL queries

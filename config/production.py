"""
Production Configuration
"""
import os
from typing import List

class ProductionConfig:
    """Production environment configuration"""
    
    # Application
    APP_NAME: str = os.getenv('APP_NAME', '玄玑AI数字员工引擎')
    APP_VERSION: str = os.getenv('APP_VERSION', '2.0')
    APP_ENVIRONMENT: str = 'production'
    DEBUG: bool = False
    
    # API
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
    API_PORT: int = int(os.getenv('API_PORT', '8080'))
    API_WORKERS: int = int(os.getenv('API_WORKERS', '4'))
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '60'))
    
    # DeepSeek
    DEEPSEEK_API_URL: str = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
    DEEPSEEK_MODEL: str = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    DEEPSEEK_API_KEY: str = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_TIMEOUT: int = int(os.getenv('DEEPSEEK_TIMEOUT', '30'))
    DEEPSEEK_MAX_RETRIES: int = int(os.getenv('DEEPSEEK_MAX_RETRIES', '3'))
    
    # Feishu
    FEISHU_APP_ID: str = os.getenv('FEISHU_APP_ID', '')
    FEISHU_APP_SECRET: str = os.getenv('FEISHU_APP_SECRET', '')
    FEISHU_ENCRYPT_KEY: str = os.getenv('FEISHU_ENCRYPT_KEY', '')
    FEISHU_VERIFICATION_TOKEN: str = os.getenv('FEISHU_VERIFICATION_TOKEN', '')
    
    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
    DB_NAME: str = os.getenv('DB_NAME', 'xuanji_engine')
    DB_USER: str = os.getenv('DB_USER', 'xuanji')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', '10'))
    DB_MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', '20'))
    DB_POOL_TIMEOUT: int = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    DB_POOL_RECYCLE: int = int(os.getenv('DB_POOL_RECYCLE', '3600'))
    
    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD', '')
    REDIS_POOL_SIZE: int = int(os.getenv('REDIS_POOL_SIZE', '10'))
    REDIS_SOCKET_TIMEOUT: int = int(os.getenv('REDIS_SOCKET_TIMEOUT', '5'))
    REDIS_SOCKET_CONNECT_TIMEOUT: int = int(os.getenv('REDIS_SOCKET_CONNECT_TIMEOUT', '5'))
    REDIS_MAX_CONNECTIONS: int = int(os.getenv('REDIS_MAX_CONNECTIONS', '50'))
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', 'json')
    LOG_OUTPUT: str = os.getenv('LOG_OUTPUT', 'stdout')
    LOG_FILE: str = os.getenv('LOG_FILE', '/var/log/xuanji-engine/app.log')
    LOG_MAX_SIZE: str = os.getenv('LOG_MAX_SIZE', '100M')
    LOG_BACKUP_COUNT: int = int(os.getenv('LOG_BACKUP_COUNT', '10'))
    
    # Monitoring
    METRICS_ENABLED: bool = os.getenv('METRICS_ENABLED', 'true').lower() == 'true'
    METRICS_PORT: int = int(os.getenv('METRICS_PORT', '9090'))
    METRICS_PATH: str = os.getenv('METRICS_PATH', '/metrics')
    HEALTH_CHECK_PATH: str = os.getenv('HEALTH_CHECK_PATH', '/health')
    READY_CHECK_PATH: str = os.getenv('READY_CHECK_PATH', '/ready')
    
    # Performance
    PERFORMANCE_MAX_CONCURRENT_REQUESTS: int = int(os.getenv('PERFORMANCE_MAX_CONCURRENT_REQUESTS', '1000'))
    PERFORMANCE_REQUEST_TIMEOUT: int = int(os.getenv('PERFORMANCE_REQUEST_TIMEOUT', '60'))
    PERFORMANCE_CONNECTION_TIMEOUT: int = int(os.getenv('PERFORMANCE_CONNECTION_TIMEOUT', '10'))
    PERFORMANCE_KEEPALIVE_TIMEOUT: int = int(os.getenv('PERFORMANCE_KEEPALIVE_TIMEOUT', '5'))
    PERFORMANCE_MAX_KEEPALIVE_CONNECTIONS: int = int(os.getenv('PERFORMANCE_MAX_KEEPALIVE_CONNECTIONS', '100'))
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', '')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS: int = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    CORS_ORIGINS: List[str] = os.getenv('CORS_ORIGINS', '').split(',')
    RATE_LIMIT_ENABLED: bool = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))

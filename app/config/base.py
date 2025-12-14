from pydantic_settings import BaseSettings
from typing import Optional

class BaseConfig(BaseSettings):
    """基础配置类"""
    # 应用配置
    APP_NAME: str = "FastAPI Product Filter"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_CHARSET: str = "utf8mb4"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

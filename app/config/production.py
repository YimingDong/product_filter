from .base import BaseConfig

class ProductionConfig(BaseConfig):
    """生产环境配置"""
    # 生产环境特定配置
    LOG_LEVEL: str = "ERROR"
    LOG_FILE: str = "/var/log/fastapi/app.log"
    
    class Config:
        env_file = ".env.production"

from .base import BaseConfig

class TestingConfig(BaseConfig):
    """测试环境配置"""
    # 测试环境特定配置
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env.testing"

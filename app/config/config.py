import os
from typing import Type
from .base import BaseConfig
from .production import ProductionConfig
from .testing import TestingConfig

# 配置映射
env_config_map = {
    "production": ProductionConfig,
    "testing": TestingConfig,
    # 默认使用基础配置
    "default": BaseConfig,
}

def get_config() -> Type[BaseConfig]:
    """获取配置类"""
    env = os.getenv("FASTAPI_ENV", "default")
    return env_config_map.get(env, BaseConfig)

# 创建配置实例
Config = get_config()()

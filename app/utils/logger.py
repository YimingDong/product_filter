import logging
import os
from logging.handlers import RotatingFileHandler
from app.config.config import Config

# 创建日志目录
if Config.LOG_FILE:
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

# 配置日志格式
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

# 创建根日志记录器
logger = logging.getLogger()
logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

# 清除默认的处理器
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# 如果配置了日志文件路径，添加文件处理器
if Config.LOG_FILE:
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

# 禁用某些第三方库的日志
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("pydantic").setLevel(logging.WARNING)

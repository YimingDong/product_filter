import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.api import api_router
from app.config.config import Config
from app.utils.logger import logger
from app.utils.error_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
import logging
# 创建FastAPI应用实例
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    description="A FastAPI product filter application with MySQL integration",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{Config.API_PREFIX}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    """记录请求信息的中间件"""
    path = request.url.path
    method = request.method
    client_host = request.client.host if request.client else "unknown"
    
    response = await call_next(request)
    
    status_code = response.status_code
    logger.info(f"Request: {method} {path} from {client_host} - Status: {status_code}")
    
    return response

# 注册API路由
app.include_router(api_router)

# 注册全局错误处理器
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 健康检查端点
@app.get("/health")
def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app_name": Config.APP_NAME,
        "version": Config.APP_VERSION
    }

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
    logger.info(f"Environment: {Config.__class__.__name__}")
    logger.info(f"API Prefix: {Config.API_PREFIX}")

# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info(f"Shutting down {Config.APP_NAME}")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

from fastapi import APIRouter
from app.api.v1 import router as v1_router
from app.config.config import Config

api_router = APIRouter()

# 包含各个版本的路由
api_router.include_router(v1_router, prefix=Config.API_PREFIX)

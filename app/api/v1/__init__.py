from fastapi import APIRouter
from app.api.v1 import products

router = APIRouter()

# 包含各个模块的路由
router.include_router(products.router, prefix="/products", tags=["products"])

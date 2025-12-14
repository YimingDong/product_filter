from fastapi import APIRouter
from app.api.v1 import products, categories, equipment

router = APIRouter()

# 包含各个模块的路由
router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(categories.router, prefix="/categories", tags=["categories"])
router.include_router(equipment.router, prefix="", tags=["equipment"])

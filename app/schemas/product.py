from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 分类模型
class CategoryBase(BaseModel):
    """分类基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="分类名称")
    description: Optional[str] = Field(None, max_length=255, description="分类描述")

class CategoryCreate(CategoryBase):
    """创建分类模型"""
    pass

class CategoryUpdate(BaseModel):
    """更新分类模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="分类名称")
    description: Optional[str] = Field(None, max_length=255, description="分类描述")

class CategoryResponse(CategoryBase):
    """分类响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 产品模型
class ProductBase(BaseModel):
    """产品基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="产品名称")
    description: Optional[str] = Field(None, max_length=255, description="产品描述")
    price: float = Field(..., gt=0, description="产品价格")
    in_stock: bool = Field(True, description="是否有库存")
    category_id: int = Field(..., description="分类ID")

class ProductCreate(ProductBase):
    """创建产品模型"""
    pass

class ProductUpdate(BaseModel):
    """更新产品模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="产品名称")
    description: Optional[str] = Field(None, max_length=255, description="产品描述")
    price: Optional[float] = Field(None, gt=0, description="产品价格")
    in_stock: Optional[bool] = Field(None, description="是否有库存")
    category_id: Optional[int] = Field(None, description="分类ID")

class ProductResponse(ProductBase):
    """产品响应模型"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    category: CategoryResponse
    
    class Config:
        from_attributes = True

# 产品过滤模型
class ProductFilter(BaseModel):
    """产品过滤模型"""
    category_id: Optional[int] = Field(None, description="分类ID")
    min_price: Optional[float] = Field(None, ge=0, description="最低价格")
    max_price: Optional[float] = Field(None, ge=0, description="最高价格")
    in_stock: Optional[bool] = Field(None, description="是否有库存")
    
    class Config:
        schema_extra = {
            "example": {
                "category_id": 1,
                "min_price": 100,
                "max_price": 1000,
                "in_stock": True
            }
        }

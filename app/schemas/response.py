from pydantic import BaseModel
from typing import Any, Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    """基础响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[T] = None
    # timestamp: datetime = datetime.now()

class PaginationResponse(BaseModel):
    """分页响应模型"""
    items: Any
    total: int
    page: int
    size: int
    pages: int

class PaginationParams(BaseModel):
    """分页参数模型"""
    page: int = 1
    size: int = 10
    
    class Config:
        schema_extra = {
            "example": {
                "page": 1,
                "size": 10
            }
        }

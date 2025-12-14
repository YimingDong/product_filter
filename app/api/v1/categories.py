from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.models import get_db
from app.schemas.product import (
    CategoryCreate, CategoryUpdate, CategoryResponse
)
from app.schemas.response import BaseResponse
from app.services.category_service import CategoryService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=BaseResponse[CategoryResponse])
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """创建分类"""
    try:
        db_category = CategoryService.create_category(db, category)
        return BaseResponse(
            code=201,
            message="Category created successfully",
            data=db_category
        )
    except ValueError as e:
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating category: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=BaseResponse[List[CategoryResponse]])
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取分类列表"""
    try:
        categories = CategoryService.get_categories(db, skip=skip, limit=limit)
        return BaseResponse(
            message="Categories retrieved successfully",
            data=categories
        )
    except Exception as e:
        logger.error(f"Error retrieving categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{category_id}", response_model=BaseResponse[CategoryResponse])
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取分类"""
    try:
        category = CategoryService.get_category(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return BaseResponse(
            message="Category retrieved successfully",
            data=category
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{category_id}", response_model=BaseResponse[CategoryResponse])
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """更新分类"""
    try:
        db_category = CategoryService.update_category(db, category_id, category)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return BaseResponse(
            message="Category updated successfully",
            data=db_category
        )
    except ValueError as e:
        logger.error(f"Error updating category {category_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{category_id}", response_model=BaseResponse[dict])
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """删除分类"""
    try:
        success = CategoryService.delete_category(db, category_id)
        if not success:
            raise HTTPException(status_code=404, detail="Category not found")
        return BaseResponse(
            message="Category deleted successfully",
            data={"id": category_id}
        )
    except ValueError as e:
        logger.error(f"Error deleting category {category_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

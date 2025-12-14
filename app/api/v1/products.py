from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import get_db
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductFilter, CategoryResponse
)
from app.schemas.response import BaseResponse, PaginationParams
from app.services.product_service import ProductService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=BaseResponse[ProductResponse])
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """创建产品"""
    try:
        db_product = ProductService.create_product(db, product)
        return BaseResponse(
            code=201,
            message="Product created successfully",
            data=db_product
        )
    except ValueError as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=BaseResponse[List[ProductResponse]])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取产品列表"""
    try:
        products = ProductService.get_products(db, skip=skip, limit=limit)
        return BaseResponse(
            message="Products retrieved successfully",
            data=products
        )
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}", response_model=BaseResponse[ProductResponse])
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取产品"""
    try:
        product = ProductService.get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return BaseResponse(
            message="Product retrieved successfully",
            data=product
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{product_id}", response_model=BaseResponse[ProductResponse])
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新产品"""
    try:
        db_product = ProductService.update_product(db, product_id, product)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return BaseResponse(
            message="Product updated successfully",
            data=db_product
        )
    except ValueError as e:
        logger.error(f"Error updating product {product_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{product_id}", response_model=BaseResponse[dict])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """删除产品"""
    try:
        success = ProductService.delete_product(db, product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return BaseResponse(
            message="Product deleted successfully",
            data={"id": product_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/filter", response_model=BaseResponse[dict])
def filter_products(
    filter_params: ProductFilter,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """过滤产品"""
    try:
        result = ProductService.filter_products(db, filter_params, pagination)
        return BaseResponse(
            message="Products filtered successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error filtering products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductFilter
from app.schemas.response import PaginationParams

class ProductService:
    """产品服务类"""
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """根据ID获取产品"""
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """获取产品列表"""
        return db.query(Product).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        """创建产品"""
        # 检查分类是否存在
        category = db.query(Category).filter(Category.id == product.category_id).first()
        if not category:
            raise ValueError(f"Category with id {product.category_id} not found")
        
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
        """更新产品"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        
        # 如果更新了分类，检查分类是否存在
        if product.category_id is not None:
            category = db.query(Category).filter(Category.id == product.category_id).first()
            if not category:
                raise ValueError(f"Category with id {product.category_id} not found")
        
        update_data = product.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """删除产品"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return False
        
        db.delete(db_product)
        db.commit()
        return True
    
    @staticmethod
    def filter_products(db: Session, filter_params: ProductFilter, pagination: PaginationParams) -> dict:
        """过滤产品"""
        query = db.query(Product)
        
        # 应用过滤条件
        if filter_params.category_id:
            query = query.filter(Product.category_id == filter_params.category_id)
        if filter_params.min_price is not None:
            query = query.filter(Product.price >= filter_params.min_price)
        if filter_params.max_price is not None:
            query = query.filter(Product.price <= filter_params.max_price)
        if filter_params.in_stock is not None:
            query = query.filter(Product.in_stock == filter_params.in_stock)
        
        # 计算总数
        total = query.count()
        
        # 应用分页
        skip = (pagination.page - 1) * pagination.size
        items = query.offset(skip).limit(pagination.size).all()
        
        # 计算总页数
        pages = (total + pagination.size - 1) // pagination.size
        
        return {
            "items": items,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }


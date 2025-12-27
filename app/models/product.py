from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Category(Base):
    """分类模型"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    products = relationship("Product", back_populates="category")

    def to_pydantic(self):
        """转换为Pydantic模型实例"""
        from app.schemas.product import CategoryResponse
        return CategoryResponse(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

class Product(Base):
    """产品模型"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False, index=True)
    in_stock = Column(Boolean, default=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    category = relationship("Category", back_populates="products")

    def to_pydantic(self):
        """转换为Pydantic模型实例"""
        from app.schemas.product import ProductResponse
        return ProductResponse(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            in_stock=self.in_stock,
            category_id=self.category_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

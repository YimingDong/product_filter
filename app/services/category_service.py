from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Category
from app.schemas.product import CategoryCreate, CategoryUpdate

class CategoryService:
    """分类服务类"""
    
    @staticmethod
    def get_category(db: Session, category_id: int) -> Optional[Category]:
        """根据ID获取分类"""
        return db.query(Category).filter(Category.id == category_id).first()
    
    @staticmethod
    def get_category_by_name(db: Session, name: str) -> Optional[Category]:
        """根据名称获取分类"""
        return db.query(Category).filter(Category.name == name).first()
    
    @staticmethod
    def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        """获取分类列表"""
        return db.query(Category).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_category(db: Session, category: CategoryCreate) -> Category:
        """创建分类"""
        # 检查分类名称是否已存在
        existing_category = db.query(Category).filter(Category.name == category.name).first()
        if existing_category:
            raise ValueError(f"Category with name '{category.name}' already exists")
        
        db_category = Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Optional[Category]:
        """更新分类"""
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        
        # 如果更新了名称，检查名称是否已存在
        if category.name and category.name != db_category.name:
            existing_category = db.query(Category).filter(Category.name == category.name).first()
            if existing_category:
                raise ValueError(f"Category with name '{category.name}' already exists")
        
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        """删除分类"""
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return False
        
        # 检查分类下是否有产品
        if db_category.products:
            raise ValueError("Cannot delete category with existing products")
        
        db.delete(db_category)
        db.commit()
        return True

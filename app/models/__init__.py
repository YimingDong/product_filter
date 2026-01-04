from .database import Base, engine, get_db
# from .product import Category, Product

# 创建所有表
Base.metadata.create_all(bind=engine)

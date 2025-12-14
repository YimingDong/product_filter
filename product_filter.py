class Product:
    def __init__(self, name, category, price, in_stock):
        self.name = name
        self.category = category
        self.price = price
        self.in_stock = in_stock
    
    def __repr__(self):
        return f"Product(name='{self.name}', category='{self.category}', price={self.price}, in_stock={self.in_stock})"

class ProductFilter:
    def __init__(self, products):
        self.products = products
    
    def filter_by_category(self, category):
        return [product for product in self.products if product.category == category]
    
    def filter_by_price_range(self, min_price, max_price):
        return [product for product in self.products if min_price <= product.price <= max_price]
    
    def filter_by_stock_status(self, in_stock):
        return [product for product in self.products if product.in_stock == in_stock]
    
    def filter(self, category=None, min_price=None, max_price=None, in_stock=None):
        filtered = self.products
        
        if category:
            filtered = [p for p in filtered if p.category == category]
        if min_price is not None:
            filtered = [p for p in filtered if p.price >= min_price]
        if max_price is not None:
            filtered = [p for p in filtered if p.price <= max_price]
        if in_stock is not None:
            filtered = [p for p in filtered if p.in_stock == in_stock]
        
        return filtered

# 示例用法
if __name__ == "__main__":
    # 创建一些产品
    products = [
        Product("智能手机A", "电子设备", 2999, True),
        Product("笔记本电脑B", "电子设备", 5999, True),
        Product("无线耳机C", "电子设备", 799, False),
        Product("运动鞋D", "服装", 499, True),
        Product("牛仔裤E", "服装", 299, True),
        Product("T恤F", "服装", 99, False),
        Product("咖啡杯G", "家居", 49, True),
        Product("抱枕H", "家居", 79, True)
    ]
    
    # 创建过滤器
    product_filter = ProductFilter(products)
    
    print("所有产品:")
    for product in products:
        print(product)
    
    print("\n过滤电子设备:")
    for product in product_filter.filter_by_category("电子设备"):
        print(product)
    
    print("\n过滤价格在100到1000之间的产品:")
    for product in product_filter.filter_by_price_range(100, 1000):
        print(product)
    
    print("\n过滤有库存的产品:")
    for product in product_filter.filter_by_stock_status(True):
        print(product)
    
    print("\n复合过滤: 服装类别，价格低于500，有库存的产品:")
    for product in product_filter.filter(category="服装", max_price=500, in_stock=True):
        print(product)

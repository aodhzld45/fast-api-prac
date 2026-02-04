from typing import Optional, List

from fastapi_product.schemas.product import Product, ProductUpdate

class ProductRepository:
    def __init__(self):
        self.products: List[Product] = []
        self.product_id = 0

    def save(self, create_product: Product) -> Product:
        self.product_id += 1
        create_product.id = self.product_id
        self.products.append(create_product)
        return create_product

    def find_all(self) -> List[Product]:
        return self.products

    def findById(self, id: int) -> Optional[Product]:
        for product in self.products:
            if product.id == id:
                return product
        return None

    def modify(self, id: int, data: ProductUpdate) -> Optional[Product]:
        product = self.findById(id)
        if not product:
            return None

        if data.product_name is not None:
            product.name = data.product_name  # alias(name) 제한
        if data.price is not None:
            product.price = data.price
        if data.discount_price is not None:
            product.discount_price = data.discount_price
        if data.stock is not None:
            product.stock = data.stock
        if data.category is not None:
            product.category = data.category

        return product

    def delete(self, id: int) -> Optional[Product]:
        for i, product in enumerate(self.products):
            if product.id == id:
                return self.products.pop(i)
        return None


product_repository = ProductRepository()

# 더미
product_repository.save(Product(name="상품1", price=20000, discount_price=1000, stock=10, category="전자"))
product_repository.save(Product(name="상품2", price=15000, discount_price=500, stock=0, category="생활"))

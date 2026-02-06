# repositories/product_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.product import Product
from models.category import Category as CategoryModel
from schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    def save(self, db: Session, data: ProductCreate) -> Product:
        # category_id 존재 검증
        category = db.get(CategoryModel, data.category_id)
        if not category:
            raise ValueError(f"카테고리 만드셈 category_id={data.category_id}")

        new_product = Product(
            name=data.product_name,  # alias(name) -> product_name
            price=data.price,
            discount_price=data.discount_price,
            stock=data.stock,
            category_id=data.category_id,
        )

        db.add(new_product)
        return new_product
    
    def find_all(
            self,
            db: Session,
            keyword: str | None = None,
            category_id: int | None = None,
            limit: int = 20,
        ):
            stmt = select(Product).options(selectinload(Product.category))

            if keyword:
                stmt = stmt.where(Product.name.contains(keyword))

            if category_id:
                stmt = stmt.where(Product.category_id == category_id)

            stmt = stmt.order_by(Product.id.desc()).limit(limit)

            return db.scalars(stmt).all()

    def find_by_id(self, db: Session, id: int):
        # 기본키(Primary Key)를 이용한 조회는 db.get이 가장 빠르고 효율적이다.
        return db.get(Product, id)
    
    def find_by_category_id(self, db: Session, category_id: int) -> list[Product]:
        stmt = (
            select(Product)
            .options(selectinload(Product.category)) 
            .where(Product.category_id == category_id)
            .order_by(Product.id.desc())
        )
        return db.scalars(stmt).all()    
    
    # Product Create Value
    # model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    # product_name: str = Field(..., min_length=2, max_length=50, alias="name")
    # price: int = Field(..., ge=100)
    # discount_price: int = Field(..., ge=0)
    # stock: int = Field(10, ge=0)

    # category_id: int = Field(..., ge=1, description="카테고리 ID")

    def update(self, db: Session, product: Product, data: ProductUpdate):
        # 이미 조회된 객체의 속성을 변경하면 세션이 이를 감지한다.
        product.name = data.product_name
        product.price = data.price
        product.discount_price = data.discount_price
        product.stock = data.stock
        product.category_id = data.category_id
        
        return product

    def delete(self, db: Session, product: Product) -> None:
        db.delete(product)


product_repository = ProductRepository()

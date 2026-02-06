# models/product.py 수정

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey 
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    discount_price: Mapped[int] = mapped_column(default=0, nullable=False) 
    stock: Mapped[int] = mapped_column(default=10, nullable=False)
    
    # 카테고리 한개가 여러개의 상품을 가지는 경우
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )
    
    @property
    def final_price(self) -> int:
        return self.discount_price
    
    @property
    def is_sold_out(self) -> bool:
        return self.stock <= 0
    


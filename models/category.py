# models/commnet.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # 카테고리 한개가 여러개의 상품을 가질 경우
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    

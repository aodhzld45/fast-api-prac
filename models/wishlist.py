# models/wishlist.py

from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .user import User

class WishList(Base):
    __tablename__ = "wish_list"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # - `user_id`: 사용자 식별자 (FK, PK)
    # - `product_id`: 상품 식별자 (FK, PK)
    # - **`created_at`**: 찜한 시점 (추가 데이터)
    
    # 각각 Product와 user를 참조하는 외래키
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # 확장 데이터: 등록일 추가 가능
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    product: Mapped["Product"] = relationship(back_populates="wish_list")
    user: Mapped["User"] = relationship(back_populates="wish_list")



    
    
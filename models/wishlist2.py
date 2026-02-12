# - user2_id: User2 식별자 (FK)
# - product_id: 상품 식별자 (FK)
# - created_at: 찜한 시점
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .user2 import User2

class WishList2(Base):
    __tablename__ = "wish_list2"
    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user2_id: Mapped[int] = mapped_column(ForeignKey("users2.id"))
    
    # 확장 데이터: 등록일 추가 가능
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    product: Mapped["Product"] = relationship(back_populates="wish_list2")
    user2: Mapped["User2"] = relationship(back_populates="wish_list2")


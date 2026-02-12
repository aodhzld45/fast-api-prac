# models/user.py

from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .wishlist2 import WishList2
    from .product import Product

class User2(Base):
    __tablename__ = "users2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    
    wish_list2: Mapped[list["WishList2"]] = relationship(back_populates="user2")
    
    product: AssociationProxy[list["Product"]] = association_proxy("wish_list2", "product")
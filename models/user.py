# models/user.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


if TYPE_CHECKING:
    from .wishlist import WishList
    from .product import Product

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    wish_list: Mapped[list["WishList"]] = relationship(back_populates="user")

    wished_products: AssociationProxy[list["Product"]] = association_proxy("wish_list", "product")

    


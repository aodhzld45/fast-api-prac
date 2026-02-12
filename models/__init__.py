# mysite4/models/__init__.py
from .user import User
from .user2 import User2
from .wishlist import WishList
from .wishlist2 import WishList2
from .product import Product
from .category import Category
from database import Base

__all__ = ["Base", "Product", "Category", "User", "WishList", "User2", "WishList2"]

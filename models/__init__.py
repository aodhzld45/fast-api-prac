# mysite4/models/__init__.py

from .product import Product
from .category import Category
from database import Base

__all__ = ["Base", "Product", "Category"]

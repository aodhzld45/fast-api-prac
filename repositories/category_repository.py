# repositories/category_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def save(self, db: Session, data: CategoryCreate) -> Category:
        new_category = Category(name=data.name)
        db.add(new_category)
        return new_category

    def find_all(self, db: Session):
        return db.scalars(select(Category)).all()

    def find_by_id(self, db: Session, id: int) -> Category | None:
        return db.get(Category, id)

    def find_by_name(self, db: Session, name: str) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        return db.scalars(stmt).first()

    def update(self, db: Session, category: Category, data: CategoryUpdate) -> Category:
        if data.name is not None:
            category.name = data.name
        return category

    def delete(self, db: Session, category: Category) -> None:
        db.delete(category)


category_repository = CategoryRepository()

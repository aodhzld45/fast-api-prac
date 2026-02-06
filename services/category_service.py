# services/category_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from models.category import Category
from models.product import Product

from repositories.category_repository import category_repository
from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryDetailResponse,
    CategoryListResponse,
)

class CategoryService:
    def create_category(self, db: Session, data: CategoryCreate) -> CategoryDetailResponse:
        exists = category_repository.find_by_name(db, data.name)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"이미 존재하는 카테고리입니다. name={data.name}",
            )

        new_category = category_repository.save(db, data)
        db.commit()
        db.refresh(new_category)
        return CategoryDetailResponse.model_validate(new_category)

    def read_categories(self, db: Session) -> CategoryListResponse:
        return category_repository.find_all(db)

    def read_category_by_id(self, db: Session, id: int) -> Category:
        category = category_repository.find_by_id(db, id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="없는 id입니다.")
        return category

    def detail_category(self, db: Session, id: int) -> CategoryDetailResponse:
        category = self.read_category_by_id(db, id)
        return CategoryDetailResponse.model_validate(category)

    def update_category(self, db: Session, id: int, data: CategoryUpdate) -> CategoryDetailResponse:
        category = self.read_category_by_id(db, id)

        if data.name is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="수정할 값이 없습니다.",
            )

        exists = category_repository.find_by_name(db, data.name)
        if exists and exists.id != category.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"이미 존재하는 카테고리입니다. name={data.name}",
            )

        updated = category_repository.update(db, category, data)
        db.commit()
        db.refresh(updated)
        return CategoryDetailResponse.model_validate(updated)

    def delete_category(self, db: Session, id: int) -> None:
        category = self.read_category_by_id(db, id)

        product_count = db.scalar(
            select(func.count()).select_from(Product).where(Product.category_id == id)
        ) or 0

        if product_count > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"해당 카테고리에 상품이 있어 삭제할 수 없습니다. productCount={product_count}",
            )

        category_repository.delete(db, category)
        db.commit()


category_service = CategoryService()

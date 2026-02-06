from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.product import Product
from models.category import Category
from schemas.product import CategoryResponse

from repositories.product_repository import product_repository
from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductDetailResponse,
    ProductListResponse,
)

class ProductService:
    def create_product(self, db: Session, data: ProductCreate) -> ProductDetailResponse:

        category = db.get(Category, data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"카테고리 없다 category_id={data.category_id}",
            )

        new_product = product_repository.save(db, data)

        db.commit()
        db.refresh(new_product)

        new_product.category = db.get(Category, new_product.category_id)

        return self._to_detail(new_product)

    def read_products(
        self,
        db: Session,
        keyword: str | None,
        category_id: int | None,
        limit: int,
    ) -> list[ProductListResponse]:
        items = product_repository.find_all(db, keyword, category_id, limit)
        return [self._to_list(p) for p in items]

    def read_product_by_id(self, db: Session, id: int):
        product = product_repository.find_by_id(db, id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "상품 없다람쥐")
        return product
    
    def read_products_by_category(self, db: Session, category_id: int) -> list[ProductListResponse]:
        category = db.get(Category, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"카테고리 없다고. category_id={category_id}",
            )

        items = product_repository.find_by_category_id(db, category_id)
        return [self._to_list(p) for p in items]
    

    def update_product(self, db: Session, id: int, data: ProductUpdate):
        # 수정할 상품 존재 여부를 먼저 확인한다.
        updated_product = self.read_product_by_id(db, id)
        
        # 레포지토리를 통해 객체 정보를 수정(더티 체크 대상)한다.
        updated_product = product_repository.update(db, updated_product, data)
        
        # 최종 확정 및 갱신
        db.commit()
        db.refresh(updated_product)
        
        return updated_product

    def delete_product(self, db: Session, id: int):
        product = self.read_product_by_id(db, id)
        
        product_repository.delete(db, product)
        
        # 삭제 트랜잭션을 확정한다.
        db.commit()

    # ---------- mapping ----------
    def _final_price(self, p: Product) -> int:
        return p.discount_price

    def _is_sold_out(self, p: Product) -> bool:
        return p.stock <= 0

    def _to_detail(self, p: Product) -> ProductDetailResponse:
        if not p.category:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="카테고리 없다고",
            )
        return ProductDetailResponse(
            id=p.id,
            name=p.name,
            final_price=self._final_price(p),
            stock=p.stock,
            is_sold_out=self._is_sold_out(p),
            category=CategoryResponse.model_validate(p.category),
        )

    def _to_list(self, p: Product) -> ProductListResponse:
        if not p.category:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="카테고리 없다고",
            )
        return ProductListResponse(
            id=p.id,
            name=p.name,
            final_price=self._final_price(p),
            category=CategoryResponse.model_validate(p.category)
        )
product_service = ProductService()

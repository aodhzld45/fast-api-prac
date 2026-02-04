from fastapi import HTTPException, status

from fastapi_product.repositories.product_repository import product_repository
from fastapi_product.schemas.product import (
    ProductCreate,
    ProductUpdate,
    Product,
    ProductDetailResponse,
    ProductListResponse,
)


class ProductService:
    def create_product(self, data: ProductCreate):
        if not data.product_name:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "name을 입력하세요."
            )
        if not data.category:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "category를 입력하세요."
            )

        if data.discount_price >= data.price:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "discount_price는 price보다 작아야 합니다."
            )

        new_product = Product(
            name=data.product_name, 
            price=data.price,
            discount_price=data.discount_price,
            stock=data.stock,
            category=data.category,
        )

        saved = product_repository.save(new_product)
        return self._to_detail(saved)

    def read_products(self):
        items = product_repository.find_all()
        return [self._to_list(p) for p in items]

    def read_product_by_id(self, id: int) -> Product:
        product = product_repository.findById(id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "없는 id입니다.")
        return product

    def detail_product(self, id: int) -> ProductDetailResponse:
        product = self.read_product_by_id(id)
        return self._to_detail(product)

    def update_product(self, id: int, data: ProductUpdate) -> ProductDetailResponse:
        self.read_product_by_id(id)

        if (
            data.product_name is None
            and data.price is None
            and data.discount_price is None
            and data.stock is None
            and data.category is None
        ):
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "수정할 값이 없습니다."
            )

        updated = product_repository.modify(id, data)
        if not updated:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "없는 id입니다.")
        if updated.discount_price >= updated.price:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "discount_price는 price보다 작아야 합니다."
            )

        return self._to_detail(updated)

    def delete_product(self, id: int):
        self.read_product_by_id(id)

        return product_repository.delete(id)

    # 계산 함수들
    def _final_price(self, p: Product) -> int:
        return p.price - p.discount_price

    def _is_sold_out(self, p: Product) -> bool:
        return p.stock <= 0

    def _to_detail(self, p: Product) -> ProductDetailResponse:
        return ProductDetailResponse(
            id=p.id,
            name=p.name,
            final_price=self._final_price(p),
            category=p.category,         
            is_sold_out=self._is_sold_out(p),
            stock=p.stock,           
        )

    def _to_list(self, p: Product) -> ProductListResponse:
        return ProductListResponse(
            id=p.id,
            name=p.name,
            final_price=self._final_price(p),
            category=p.category,
        )


product_service = ProductService()

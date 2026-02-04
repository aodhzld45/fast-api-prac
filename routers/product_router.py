from typing import Optional, List

from fastapi import APIRouter, status, Path, Query

from fastapi_product.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductDetailResponse,
    ProductListResponse,
)
from fastapi_product.services.product_service import product_service

router = APIRouter(prefix="/products-mvc", tags=["products-mvc"])


@router.post("", response_model=ProductDetailResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate):
    return product_service.create_product(data)


@router.get("", response_model=List[ProductListResponse])
def read_product_list(
    keyword: Optional[str] = Query(None, min_length=2),
    p_category: Optional[str] = Query(None, alias="p-category"),
    limit: int = Query(20, ge=1, le=100),
):
    items = product_service.read_products()

    # keyword (name 기준)
    if keyword:
        items = [x for x in items if keyword in x.name]

    # category filter
    if p_category:
        items = [x for x in items if x.category == p_category]

    # limit
    items = items[:limit]

    return items


@router.get("/{product_id}", response_model=ProductDetailResponse)
def detail_product(product_id: int = Path(..., ge=1)):
    return product_service.detail_product(product_id)


@router.put("/{product_id}", response_model=ProductDetailResponse)
def update_product(
    product_id: int = Path(..., ge=1),
    data: ProductUpdate = ...,
):
    return product_service.update_product(product_id, data)


@router.delete("/{product_id}")
def delete_product(product_id: int = Path(..., ge=1)):
    return product_service.delete_product(product_id)

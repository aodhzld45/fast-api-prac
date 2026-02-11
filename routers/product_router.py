from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductDetailResponse
)
from services.product_service import product_service

router = APIRouter(prefix="/products", tags=["Product"])

@router.post(
    "",
    response_model=ProductDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
):
    return product_service.create_product(db, data)

# @router.get("", response_model=list[ProductListResponse])
# def read_product_list(db: Session = Depends(get_db)):
#     return product_service.read_products(db)

@router.get("", response_model=list[ProductListResponse])
def read_products(
    db: Session = Depends(get_db),
    keyword: Annotated[str | None, Query(min_length=2)] = None,
    category: Annotated[str | None, Query(alias="p-category")] = None,
    limit: Annotated[int, Query()] = 20
):
    return product_service.read_products(db, keyword, category, limit)

# 조회 쿼리 향상
@router.get("/with-categories", response_model=list[ProductListResponse])
def read_products_with_categories(
    db: Session = Depends(get_db),
    keyword: Annotated[str | None, Query(min_length=2)] = None,
    category: Annotated[str | None, Query(alias="p-category")] = None,
    limit: Annotated[int, Query()] = 20
):
    return product_service.read_categories_with(db, keyword, category, limit)

@router.get("/{id}", response_model=ProductDetailResponse)
def read_product(id: int, db: Session = Depends(get_db)):
    return product_service.read_product_by_id(db, id)

# 조회 쿼리 성능 향상
@router.get("/with/{id}", response_model=ProductDetailResponse)
def read_product_with(id: int, db: Session = Depends(get_db)):
    return product_service.read_products_with_category_id(db, id)

@router.put("/{id}", response_model=ProductDetailResponse)
def update_product(id: int, data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.update_product(db, id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, id)


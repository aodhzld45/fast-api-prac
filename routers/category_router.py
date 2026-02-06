from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.product import ProductListResponse

from schemas.category import (
    CategoryCreate,
    CategoryDetailResponse,
    CategoryListResponse,
)
from services.category_service import category_service
from services.product_service import product_service

router = APIRouter(prefix="/categories", tags=["Category"])

@router.post(
    "",
    response_model=CategoryDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
):
    return category_service.create_category(db, data)

@router.get("", response_model=list[CategoryListResponse])
def read_categories(db: Session = Depends(get_db)):
    return category_service.read_categories(db)

@router.get("/{category_id}/products", response_model=list[ProductListResponse])
def read_products_in_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return product_service.read_products_by_category(db, category_id)


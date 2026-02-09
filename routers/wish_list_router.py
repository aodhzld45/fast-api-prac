from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db  # 경로 맞게 조정
from schemas.wishlist import WishlistCreateResponse, WishlistItemResponse

from services.wish_list_service import wish_list_service

router = APIRouter(tags=["Wishlist"])


@router.post(
    "/users/{user_id}/wishlist/{product_id}",
    response_model=WishlistCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_to_wishlist(
    user_id: int,
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        return wish_list_service.add_to_wishlist(db, user_id, product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get(
    "/users/{user_id}/wishlist",
    response_model=list[WishlistItemResponse],
)
def read_user_wishlist(user_id: int, db: Session = Depends(get_db)):
    try:
        return wish_list_service.read_user_wishlist(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.delete(
    "/users/{user_id}/wishlist/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_from_wishlist(user_id: int, product_id: int, db: Session = Depends(get_db)):
    try:
        wish_list_service.remove_from_wishlist(db, user_id, product_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

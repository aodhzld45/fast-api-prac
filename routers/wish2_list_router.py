from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db 
from schemas.wishlist2 import WishList2Create, WishList2DetailResponse
from services.wish2_list_service import wish2_list_service
from dependencies import get_current_user
from models.user2 import User2


router = APIRouter(prefix="/wishlist2", tags=["Wishlist"])

@router.post("", response_model=WishList2DetailResponse, status_code=status.HTTP_201_CREATED)
def create_wish(
        product_id: int = Query(..., description="추가할 상품의 ID"),
        db: Session = Depends(get_db),
        current_user: User2 = Depends(get_current_user),
    ):
    return wish2_list_service.add_to_wishlist(
        db=db, 
        user2_id=current_user.id, 
        product_id=product_id
    )

@router.get("/me/products", response_model=list[WishList2DetailResponse])
def read_my_products(
    db: Session = Depends(get_db),
    current_user: User2 = Depends(get_current_user),
):
    """내가 찜한 상품 목록 조회"""
    return wish2_list_service.get_my_wishlist(db, current_user.id)

@router.delete("/{product_id}", response_model=list[WishList2DetailResponse])
def delete_wishlist_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):

    result = wish2_list_service.remove_from_wishlist(
        db=db, 
        user_id=current_user.id, # 토큰에서 가져온 유저 ID
        product_id=product_id
    )
    return result
from sqlalchemy.orm import Session

from repositories.wish_list_repository import wish_list_repository
from models.wishlist import WishList


class WishListService:
    def add_to_wishlist(self, db: Session, user_id: int, product_id: int) -> WishList:
        link = wish_list_repository.add(db, user_id, product_id)

        db.commit()
        db.refresh(link)

        return link
    
    # 목록 조회
    def read_user_wishlist(self, db: Session, user_id: int) -> list[WishList]:
        return wish_list_repository.find_by_user(db, user_id)

    # 삭제
    def remove_from_wishlist(self, db: Session, user_id: int, product_id: int) -> None:
        wish_list_repository.delete(db, user_id, product_id)
        db.commit()

wish_list_service = WishListService()

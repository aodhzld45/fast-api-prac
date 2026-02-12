from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.wishlist2 import WishList2
from repositories.wish2_list_repository import wish2_list_repository
from repositories.product_repository import product_repository # 상품 존재 확인용

class WishList2Service:
    def add_to_wishlist(self, db: Session, user2_id: int, product_id: int):
        existing_wish = wish2_list_repository.find_by_user_and_product(db, user2_id, product_id)
        if existing_wish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="이미 위시리스트에 추가된 상품입니다."
            )

        new_wish = WishList2(
            user2_id=user2_id,
            product_id=product_id
        )
        
        wish2_list_repository.save(db, new_wish)
        db.commit() # 레포지토리에서 commit을 안 하므로 서비스에서 실행
        db.refresh(new_wish)
        
        return new_wish

    def get_my_wishlist(self, db: Session, user_id: int):
        return wish2_list_repository.find_all_by_user_id(db, user_id)

    def remove_from_wishlist(self, db: Session, user_id: int, product_id: int):
        wish_item = wish2_list_repository.find_by_user_and_product(db, user_id, product_id)
        
        if not wish_item:
            raise HTTPException(status_code=404, detail="위시리스트 없음")
            
        wish2_list_repository.delete(db, wish_item)
        db.commit()
        return {"message": "위시리스트에서 삭제되었습니다."}

wish2_list_service = WishList2Service()

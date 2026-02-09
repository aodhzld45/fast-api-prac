from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from models.user import User
from models.product import Product
from models.wishlist import WishList

class WishListRepository:
    def exists(self, db: Session, user_id: int, product_id: int) -> bool:
        q = select(WishList.id).where(
            WishList.user_id == user_id,
            WishList.product_id == product_id,
        )
        return db.scalar(q) is not None

    def add(self, db: Session, user_id: int, product_id: int) -> WishList:
        # user 존재 검증
        user = db.get(User, user_id)
        if not user:
            raise ValueError(f"유저가 없다람쥐. user_id={user_id}")

        # product 존재 검증
        product = db.get(Product, product_id)
        if not product:
            raise ValueError(f"상품이 없다람쥐 product_id={product_id}")

        # 중복 찜 방지
        if self.exists(db, user_id, product_id):
            raise ValueError(f"이미 찜한 상품 user_id={user_id}, product_id={product_id}")

        link = WishList(user_id=user_id, product_id=product_id)
        db.add(link)
        return link
    # [GET] /users/{user_id}/wishlist: 특정 사용자의 위시리스트 목록 조회
    def find_by_user(self, db: Session, user_id: int) -> list[WishList]:
        # 유저 존재 검증
        user = db.get(User, user_id)
        if not user:
            raise ValueError(f"유저가 없다람쥐. user_id={user_id}")

        q = (
            select(WishList)
            .where(WishList.user_id == user_id)
            .options(selectinload(WishList.product))  # product 같이 로드
            .order_by(WishList.created_at.desc())
        )
        return list(db.scalars(q).all())

    # [DELETE] /users/{user_id}/wishlist/{product_id}: 위시리스트 삭제 (찜 취소)
    def delete(self, db: Session, user_id: int, product_id: int) -> None:
        q = select(WishList).where(
            WishList.user_id == user_id,
            WishList.product_id == product_id,
        )
        link = db.scalar(q)
        if not link:
            raise ValueError(f"찜 내역이 없다람쥐. user_id={user_id}, product_id={product_id}")

        db.delete(link)


wish_list_repository = WishListRepository()
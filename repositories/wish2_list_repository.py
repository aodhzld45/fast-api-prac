from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from models.wishlist2 import WishList2

class WishList2Repository:
    def save(self, db: Session, new_wish: WishList2):
        db.add(new_wish)
        return new_wish

    def find_all_by_user_id(self, db: Session, user2_id: int):
        return db.scalars(
            select(WishList2)
            .options(joinedload(WishList2.product))
            .where(WishList2.user2_id == user2_id)
        ).all()

    def find_by_user_and_product(self, db: Session, user2_id: int, product_id: int):
        return db.scalars(
            select(WishList2).where(
                and_(
                    WishList2.user2_id == user2_id,
                    WishList2.product_id == product_id
                )
            )
        ).first()

    def find_by_id(self, db: Session, id: int):
        return db.get(WishList2, id)

    def delete(self, db: Session, wish_item: WishList2):
        db.delete(wish_item)

wish2_list_repository = WishList2Repository()

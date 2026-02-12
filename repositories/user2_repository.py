from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user2 import User2

class User2Repository:
    def save(self, db: Session, user: User2):
        db.add(user)
        return user

    def find_by_email(self, db: Session, email: str):
        stmt = select(User2).where(User2.email == email)
        return db.scalars(stmt).first()

    def find_by_id(self, db: Session, user_id: int):
        return db.get(User2, user_id)
    
user2_repository = User2Repository()
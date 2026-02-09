from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user import User 
from schemas.user import UserCreate

class UserRepository:
    def save(self, db: Session, data: UserCreate) -> User:
        # nickname 중복 체크
        exists = db.scalar(select(User).where(User.nickname == data.nickname))
        if exists:
            raise ValueError(f"이미 존재하는 닉네임임. nickname={data.nickname}")

        new_user = User(
            nickname=data.nickname
        )
        db.add(new_user)
        return new_user

    def find_all(self, db: Session) -> list[User]:
        return list(db.scalars(select(User).order_by(User.id.desc())).all())
    
user_repository = UserRepository()

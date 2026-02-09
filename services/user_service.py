from sqlalchemy.orm import Session
from repositories.user_repository import user_repository
from schemas.user import UserCreate

class UserService:
    def create_user(self, db: Session, data: UserCreate):
        user = user_repository.save(db, data)
        db.commit()
        db.refresh(user)
        return user

    def read_users(self, db: Session):
        return user_repository.find_all(db)
    

user_service = UserService()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db   # 프로젝트 경로에 맞게 조정
from schemas.user import UserCreate, UserResponse
from services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(db, data)


@router.get("", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db),
):
    return user_service.read_users(db)

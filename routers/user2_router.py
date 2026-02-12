from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.user2 import User2Response
from models.user2 import User2
# from schemas.post2 import Post2ListResponse
from dependencies import get_current_user
from services.user_service import user_service

router = APIRouter(prefix="/user2" ,tags=["Login"])

@router.get("/me", response_model=User2Response)
def get_me(current_user: User2 = Depends(get_current_user)):
    return current_user

# @router.get("/me/posts", response_model=list[Post2ListResponse])
# def read_my_posts(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """내가 작성한 게시글 목록 조회"""
#     return user_service.read_posts_by_user_id(db, current_user.id)
    
    
# @router.get("/users/{user_id}/posts", response_model=list[Post2ListResponse])
# def read_posts_by_user(user_id: int, db: Session = Depends(get_db)):
#     """특정 유저가 작성한 게시글 목록 조회"""
#     return user_service.read_posts_by_user_id(db, user_id)
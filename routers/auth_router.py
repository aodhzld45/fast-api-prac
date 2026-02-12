# routers/auth_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import auth_service
from schemas.user2 import (
    User2Create,
    User2Response,
    TokenResponse,
    User2Login
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=User2Response, status_code=status.HTTP_201_CREATED)
def signup(data: User2Create, db: Session = Depends(get_db)):
    return auth_service.signup(db, data)

@router.post("/login", response_model=TokenResponse)
def login(data: User2Login, db: Session = Depends(get_db)):
    access_token = auth_service.login(db, data)
    return {"access_token": access_token}



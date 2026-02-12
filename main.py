# app/main.py
from fastapi import FastAPI
from routers.product_router import router as product_router
from routers.category_router import router as category_router
from routers.user_router import router as user_router
from routers.user2_router import router as user2_router
from routers.auth_router import router as auth_router
from routers.wish_list_router import router as wish_list_router
from routers.wish2_list_router import router as wish2_list_router
import models

# DB 연결 설정 부분
from database import engine, Base

# 기존 테이블 지우기 -> drop table 하고 싶을 때
#Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)
 
app = FastAPI()

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(user2_router)
app.include_router(wish_list_router)
app.include_router(wish2_list_router)

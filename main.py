# app/main.py
from fastapi import FastAPI
from routers.product_router import router as product_router
from routers.category_router import router as category_router
import models

# DB 연결 설정 부분
from database import engine, Base

# 기존 테이블 지우기 -> drop table 하고 싶을 때
#Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)
 
app = FastAPI()

app.include_router(category_router)
app.include_router(product_router)





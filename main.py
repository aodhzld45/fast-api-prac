# app/main.py
from fastapi import FastAPI
from fastapi_product.routers.product_router import router as product_router
app = FastAPI()

app.include_router(product_router)




from datetime import datetime
from pydantic import BaseModel

class WishlistCreateResponse(BaseModel):
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        

class ProductListResponse(BaseModel):
    id: int
    name: str
    price: int
    discount_price: int
    stock: int
    category_id: int

    class Config:
        from_attributes = True


class WishlistItemResponse(BaseModel):
    created_at: datetime
    product: ProductListResponse

    class Config:
        from_attributes = True
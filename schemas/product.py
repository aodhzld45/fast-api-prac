from pydantic import BaseModel, Field, model_validator
from typing import Optional

class Product:
    def __init__(self, name, price, discount_price, stock, category):
        self.name = name
        self.price = price
        self.discount_price = discount_price
        self.stock = stock
        self.category = category
        
class ProductCreate(BaseModel):
    product_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        alias="name",
    )
    price: int = Field(..., ge=100)
    discount_price: int = Field(..., ge=0)
    stock: int = Field(10, ge=0)
    category: str = Field(..., min_length=2)

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.discount_price >= self.price:
            raise ValueError("discount_price는 price보다 작아야 합니다.")
        return self
    
class ProductUpdate(BaseModel):
    # 부분 수정 허용(Optional)
    product_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        alias="name",
    )
    price: Optional[int] = Field(None, ge=100)
    discount_price: Optional[int] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=2)

    @model_validator(mode="after")
    def validate_discount_price(self):
        # 둘 다 들어온 경우에만 비교
        if self.price is not None and self.discount_price is not None:
            if self.discount_price >= self.price:
                raise ValueError("discount_price는 price보다 작아야 합니다.")
        return self

    class Config:
        populate_by_name = True    
    
class ProductDetailResponse(BaseModel):
    id: int
    name: str
    final_price: int
    category: str
    stock: int
    is_sold_out: bool
    
class ProductListResponse(BaseModel):
    id: int
    name: str
    final_price: int
    category: str  
    

    
    
    
      
        
        
    

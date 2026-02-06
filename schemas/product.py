from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class ProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    product_name: str = Field(..., min_length=2, max_length=50, alias="name")
    price: int = Field(..., ge=100)
    discount_price: int = Field(..., ge=0)
    stock: int = Field(10, ge=0)

    category_id: int = Field(..., ge=1, description="카테고리 ID")

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.discount_price >= self.price:
            raise ValueError("discount_price는 price보다 작아야 합니다.")
        return self


class ProductUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    product_name: Optional[str] = Field(None, min_length=2, max_length=50, alias="name")
    price: Optional[int] = Field(None, ge=100)
    discount_price: Optional[int] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)

    category_id: Optional[int] = Field(None, ge=1, description="카테고리 ID")

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.price is not None and self.discount_price is not None:
            if self.discount_price >= self.price:
                raise ValueError("discount_price는 price보다 작아야 합니다.")
        return self

class ProductDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    final_price: int
    stock: int
    is_sold_out: bool
    
    category: CategoryResponse

class ProductListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    final_price: int
    
    category: CategoryResponse



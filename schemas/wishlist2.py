from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .product import ProductListResponse
from .user2 import User2Response
# ProductResponse 스키마가 있다면 임포트하세요. 없으면 기본 정보를 담습니다.
# from .product import ProductResponse 

class WishList2Create(BaseModel):
    product_id: int

class WishList2Response(BaseModel):
    id: int
    product_id: int
    user2_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WishList2DetailResponse(BaseModel):
    id: int
    user2: User2Response
    product: ProductListResponse
    product_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# 만약 위시리스트에 메모 기능을 넣고 싶다면 title, content를 추가한 버전
class WishList2WithMemoResponse(BaseModel):
    id: int
    product_id: int
    # 위시리스트 모델에 title, content 컬럼을 추가했을 경우 사용
    # title: str 
    # content: str
    user2: User2Response
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

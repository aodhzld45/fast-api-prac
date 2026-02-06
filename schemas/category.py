from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

# - **CategoryCreate**: `name` (2~20자)
# - **CategoryRead**: `id`, `name`
class CategoryCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., min_length=2, max_length=50)


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, min_length=2, max_length=50)

class CategoryResponse(BaseModel):
    # SQLAlchemy Category 객체를 그대로 읽기 위해
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class CategoryDetailResponse(CategoryResponse):
    pass

class CategoryListResponse(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)




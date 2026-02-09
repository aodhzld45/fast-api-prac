from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=2, max_length=50)

class UserResponse(BaseModel):
    id: int
    nickname: str

    class Config:
        from_attributes = True
# schemas/user2.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class User2Create(BaseModel):
    email: EmailStr
    nickname : str
    password: str


class User2Response(BaseModel):
    id: int
    email: str
    nickname: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
# schemas/user2.py에 로그인 관련 스키마를 추가한다.
class User2Login(BaseModel):
    email: str
    nickname : str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
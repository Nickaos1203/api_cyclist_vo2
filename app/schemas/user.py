from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    pseudo: str
    email: str
    password:str
    is_coach: int


class UserLogin(BaseModel):
    email: str
    password:str


class UserRead(BaseModel):
    pseudo: Optional[str] = None
    email: str
    password:str
    is_coach: int


class UserUpdate(BaseModel):
    pseudo: Optional[str] = None
    email: Optional[str] = None
    is_coach: Optional[int] = None


class UserUpdatePassword(BaseModel):
    password: Optional[str] = None


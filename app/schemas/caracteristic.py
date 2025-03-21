from pydantic import BaseModel
from typing import Optional

class CaracteristicCreate(BaseModel):
    gender: str
    age: int
    weight: float
    height: float


class CaracteristicUpdate(BaseModel):
    gender: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
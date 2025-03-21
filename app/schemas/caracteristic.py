from pydantic import BaseModel
from typing import Optional

class CaracteristicCreate(BaseModel):
    gender: int
    age: int
    weight: float
    height: float
    id_user: int


class CaracteristicUpdate(BaseModel):
    gender: Optional[int] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
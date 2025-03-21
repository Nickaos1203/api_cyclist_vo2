from pydantic import BaseModel
from typing import Optional

class TestTypeCreate(BaseModel):
    name_type: str


class TestCreate(BaseModel):
    power_max: float
    hr_max: float
    vo2_max: float
    rf_max: float
    cadence_max: float
    id_test_type: int


class TestUpdate(BaseModel):
    id: int
    power_max: Optional[float] = None
    hr_max: Optional[float] = None
    vo2_max: Optional[float] = None
    rf_max: Optional[float] = None
    cadence_max: Optional[float] = None
    id_test_type: Optional[int] = None
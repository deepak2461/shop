


from pydantic import BaseModel, Field, field_validator , ConfigDict
from datetime import datetime
from typing import Optional

class SalesRequest(BaseModel):
    start_date : datetime = Field(default_factory=lambda: datetime.now() - datetime.timedelta(days=30))
    end_date : datetime = Field(server_default = datetime.now())

    model_config = ConfigDict(from_attributes=True)

class SalesResponse(BaseModel):
    total_sales : float
    total_orders : int
    avg_order : float

    model_config = ConfigDict(from_attributes=True)

class SalesResponseV(BaseModel):
    data : SalesResponse
    message : str

    model_config = ConfigDict(from_attributes=True)

class MonthlyRequest(BaseModel):
    months : int

    @field_validator("months")
    def validate_month(cls, value):
        if value < 1 or value > 12:
            raise ValueError("Month must be between 1 and 12")
        return value
    

    model_config = ConfigDict(from_attributes=True)



class MonthStat(BaseModel):
    month : str
    year : int
    total_sales : float
    total_orders : int
    avg_order : float

    model_config = ConfigDict(from_attributes=True)

class MonthlyResponse(BaseModel):
    data : list[MonthStat]


class MonthlyResponseV(BaseModel):
    data : MonthlyResponse
    message : str

class CategoryStat(BaseModel):
    category : str
    total_sales : float
    pct : float         # Percentage share of total revenue (0–100)
    total_orders : int

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    data : list[CategoryStat]


class CategoryResponseV(BaseModel):
    data : CategoryResponse
    message : str



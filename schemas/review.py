

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List

class ReviewCreate(BaseModel):
    rating: float
    text: str

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user: str 
    rating: float
    text: str
    date: datetime 

    model_config = ConfigDict(from_attributes=True)


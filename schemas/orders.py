

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

import enums

class OrderItemCreate(BaseModel):
    product_id : int
    quantity : int

class OrderItemResponse(OrderItemCreate):
    name : str
    price : float
    subtotal : float

    model_config = ConfigDict(from_attributes=True)



class OrderCreate(BaseModel):
    items : List[OrderItemCreate]
    message : str

class OrderResponse(BaseModel):
    id : str
    customer : str
    email : str
    items : List[OrderItemResponse]
    item_count : int
    total : float
    status : str
    created_at : datetime

    model_config = {"from_attributes": True}

class OrderResponseV(OrderResponse):
    message : str
    
class OrderStatusUpdate(BaseModel):
    status : enums.OrderStatus

class OrderListResponse(BaseModel):
    orders : List[OrderResponse]
    total : int
    page : int
    limit : int

class OrderListResponseV(OrderListResponse):
    message : str

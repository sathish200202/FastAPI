from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SingleProductOrder(BaseModel):
    product_id: int
    quantity: int

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float


    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime
    # order_items: list[OrderItemOut]


    class Config:
        orm_mode = True
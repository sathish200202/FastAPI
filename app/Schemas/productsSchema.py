from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    product_name: str
    price: float
    category: str
    quantity: int


class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True
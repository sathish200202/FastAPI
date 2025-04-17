from pydantic import BaseModel, Field
from typing import Optional


class CartCreate(BaseModel):
    product_id: int = Field(..., title="Product ID")
    quantity: int = Field(..., title="Quantity of Product")


class updateQuantity(BaseModel):
    quantity: Optional[int] = Field(1, title="Quantity of Product")


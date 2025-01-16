from pydantic import BaseModel, EmailStr
from typing import Optional, List

class OrderItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    products: List[OrderItem]

class OrderUpdate(BaseModel):
    order_status: Optional[str] 
    products: Optional[List[OrderItem]] 

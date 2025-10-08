from pydantic import BaseModel
from typing import List

class ProductCreate(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int
    products: List[ProductCreate]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: float
    status: str

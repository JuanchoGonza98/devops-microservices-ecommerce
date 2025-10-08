from pydantic import BaseModel
from typing import List

class ProductItem(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    id: int
    user_id: int
    products: List[ProductItem]
    total: float
    status: str = "pending"

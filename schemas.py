from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserOut(UserCreate):
    id: int
    class Config:
        from_attributes = True

# Product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0

class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True

# Order
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemOut]
    class Config:
        from_attributes = True

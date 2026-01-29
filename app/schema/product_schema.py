from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name:str
    price:float
    is_active:bool=True
    description:str

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    is_active: bool
    description: str
    created_at: datetime
    updated_at: datetime

class ProductDetailResponse(BaseModel):
    id:int
    name:str
    price:float
    is_active:bool
    description:str
    current_stock_quantity: int

class ProductUpdate(BaseModel):
    price:float








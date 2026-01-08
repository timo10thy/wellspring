from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SaleCreate(BaseModel):
    stock_id: int
    quantity_sold: int
    selling_price: float


class SaleResponse(BaseModel):
    id: int
    stock_id: int
    quantity_sold: int
    selling_price: float
    total_amount: float
    created_at: datetime

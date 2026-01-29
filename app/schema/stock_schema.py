from pydantic import BaseModel
from typing import Optional
from datetime import datetime,date

class StockCreate(BaseModel):
    product_id:int
    quantity: int
    cost_price:float
    expiry_date: Optional[date] = None


class StockResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    cost_price:float
    expiry_date: Optional[date] = None
    created_at:datetime
    updated_at:datetime

class StockConsumptionReport(BaseModel):
    stock_id:int
    product_name:str
    current_quantity:int
    initial_stock_quantity:int
    total_quantity_sold:int
    average_daily_consumption:float
    estimated_days_remaining:int

    

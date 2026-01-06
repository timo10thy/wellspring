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
# _tablename__='stocks'
#     id = Column(Integer,primary_key=True,nullable=False,index=True)
#     product_id= Column(Integer, ForeignKey('products.id', ondelete='CASCADE'),nullable=False)
#     quantity= Column(Integer, nullable=False)
#     cost_price = Column(Numeric(10,2), nullable=False)
#     expiry_date = Column(Date, nullable=True)
#     created_at = Column(DateTime(timezone=True),server_default=func.now(), nullable=False)
#     updated_at = Column(
#         DateTime(timezone=True), 
#         server_default=func.now(), 
#         onupdate=func.now(), nullable= False
#     )

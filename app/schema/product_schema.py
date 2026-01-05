from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# class Products(Base):
#     __tablename__='products'
#     id= Column(Integer, primary_key= True, nullable=False, index=True)
#     name= Column(String(200), unique=True, nullable=False)
#     price = Column(Decimal(10,2), nullable=False)
#     is_active= Column(Boolen, nullable=False, default=True, server_default='1')
#     description= Column(String(500), nullable=False)
#     created_at = Column(Datetime(timezone=True),server_default=func.now(), nullable= False)
#     updated_at = Column(Datetime(timezzone=True),server_default=func.now, onupdate=func.now, nullable= False
#     )

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







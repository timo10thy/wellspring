from fastapi import FastAPI
from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, func,Numeric,Boolean
from sqlalchemy.orm import relationship

# id → identity
# name → what is being sold
# price → current selling price
# is_active → can this be sold?
# created_at
# updated_at
# Optional (but realistic):
# expires_at
# sku or internal code
# description

class Products(Base):
    __tablename__='products'
    id= Column(Integer, primary_key= True, nullable=False, index=True)
    name= Column(String(200), unique=True, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    is_active= Column(Boolean, nullable=False, default=True, server_default='1')
    description= Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now, nullable= False
    )



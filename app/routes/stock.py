from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.users import User
from typing import Annotated
from app.schema.stock_schema import StockCreate,StockResponse
from app.routes.basemodel import get_db
from app.middlewares.admin import admin_validation
from app.models.users import User
from app.models.products import Products
from app.models.stock import Stocks
import logging


logger=logging.getLogger(__name__)
router=APIRouter(prefix='/stock',tags=['Stock'])
@router.post('/create', response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def stock_create(stock_data: StockCreate,db: Session = Depends(get_db),current_admin: User = Depends(admin_validation)):
    
    if stock_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock quantity must be greater than zero"
        )

    if stock_data.cost_price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cost price must be greater than zero"
        )

   
    try:
        product = db.query(Products).filter(
            Products.id == stock_data.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        
        new_stock = Stocks(
            product_id=stock_data.product_id,
            quantity=stock_data.quantity,
            cost_price=stock_data.cost_price,
            expiry_date=stock_data.expiry_date
        )

        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)

        return new_stock

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create stock"
        )

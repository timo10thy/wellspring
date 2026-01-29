from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.users import User
from typing import Annotated
from app.schema.stock_schema import StockCreate,StockResponse,StockConsumptionReport
from app.routes.basemodel import get_db
from app.middlewares.admin import admin_validation
from app.models.users import User
from app.models.products import Products
from app.models.stock import Stocks
from app.models.sales import Sales
from datetime import datetime,date
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


@router.get("/{stock_id}/consumption",response_model=StockConsumptionReport,status_code=status.HTTP_200_OK)
def check_consumption(stock_id: int,db: Session = Depends(get_db),current_admin: User = Depends(admin_validation)):
    stock = db.query(Stocks).filter(Stocks.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )
    
    product = stock.product
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product for this stock not found"
        )

    sales = db.query(Sales).filter(Sales.stock_id == stock.id).all()
    total_quantity_sold = sum(sale.quantity_sold for sale in sales)
    initial_stock_quantity = stock.quantity + total_quantity_sold
    if sales:
        first_sale_date = min(sale.created_at.date() for sale in sales)
        days_active = (date.today() - first_sale_date).days or 1
        average_daily_consumption = total_quantity_sold / days_active
    else:
        average_daily_consumption = 0
    if average_daily_consumption > 0:
        estimated_days_remaining = int(stock.quantity / average_daily_consumption)
    else:
        estimated_days_remaining = 0

    return {
        "stock_id": stock.id,
        "product_name": product.name,
        "current_quantity": stock.quantity,
        "initial_stock_quantity": initial_stock_quantity,
        "total_quantity_sold": total_quantity_sold,
        "average_daily_consumption": round(average_daily_consumption, 2),
        "estimated_days_remaining": estimated_days_remaining
    }

@router.post('/add/stock', response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def new_stock(
    stock_data: StockCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(admin_validation)
):
    
    product = db.query(Products).filter(Products.id == stock_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product does not exist")

    
    existing_stock = db.query(Stocks).filter(
        Stocks.product_id == stock_data.product_id,
        Stocks.cost_price == stock_data.cost_price,
        Stocks.expiry_date == stock_data.expiry_date
    ).first()

    if existing_stock:
        
        existing_stock.quantity += stock_data.quantity
        db.add(existing_stock)
        db.commit()
        db.refresh(existing_stock)
        return existing_stock
    else:
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



def get_total_stock_quantity(product_id: int, db: Session):
    all_stocks = db.query(Stocks).filter(Stocks.product_id == product_id).all()
    return sum(stock.quantity for stock in all_stocks)


    
    

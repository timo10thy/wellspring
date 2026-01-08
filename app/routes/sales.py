from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import date
from app.routes.basemodel import get_db
from app.models.users import User
from app.models.sales import Sales
from app.models.stock import Stocks
from app.models.products import Products
from app.middlewares.auth import AuthMiddleware
from app.schema.sales_schema import SaleCreate, SaleResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sales", tags=["Sales"])
db_dependency = Annotated[Session, Depends(get_db)]
@router.post("/create", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sales(sales_data: SaleCreate,db: db_dependency,current_user: User = Depends(AuthMiddleware)):
    try:
       
        stock = db.query(Stocks).filter(Stocks.id == sales_data.stock_id).first()
        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found"
            )

        if stock.expiry_date and stock.expiry_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot sell expired stock"
            )

        if sales_data.quantity_sold <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sale quantity must be greater than zero"
            )

        if stock.quantity < sales_data.quantity_sold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )

        product = db.query(Products).filter(Products.id == stock.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product for this stock not found"
            )
        selling_price = product.price

        sale = Sales(
            stock_id=stock.id,
            sold_by=current_user.id,
            quantity_sold=sales_data.quantity_sold,
            selling_price=selling_price,
            total_amount=sales_data.quantity_sold * selling_price
        )
        db.add(sale)

        stock.quantity -= sales_data.quantity_sold
        db.add(stock)
        db.commit()
        db.refresh(sale)

        return sale

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create sale: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create sale"
        )

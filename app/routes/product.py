from fastapi import APIRouter, Depends, status, HTTPException
from app.schema.product_schema import ProductCreate,ProductResponse
from sqlalchemy.orm import Session
from app.routes.basemodel import get_db
from app.models.users import User
from app.models.products import Products
from app.middlewares.admin import admin_validation
from typing import Annotated
from sqlalchemy.orm import relationship
import logging
import bcrypt

logger=logging.getLogger(__name__)
router= APIRouter(prefix='/product',tags=['Product'])

@router.post('/create',response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
def product_create(product_data:ProductCreate, db:Session=Depends(get_db),current_admin: User = Depends(admin_validation)):
    try:
        current_product = db.query(Products).filter(Products.name == product_data.name).first()
        if current_product:
            raise HTTPException(status_code=400,detail="Product name alrealdy exit")
        new_product= Products(
            name=product_data.name,
            price= product_data.price,
            is_active=product_data.is_active,
            description=product_data.description
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500,detail='Fail to create product')



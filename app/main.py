from fastapi import FastAPI
from app.models.users import User
from app.routes.user_route import router as user_route
from app.routes.auth import router as auth
from app.routes.admin import router as admin
from app.routes.product import router as products
from app.routes.stock import router as stock
from app.routes.sales import router as sale
from app.routes.basemodel import engine
from app.models.base import Base
import logging



logger=logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    tittle= "Well Spring App",
    version= "1",
    description= 'dailly transaction'
)


@app.get("/home")
def homepage():
    return {
        "success: Your daily transaction and record as he dey hot"
    }
app.include_router(user_route)
app.include_router(auth)
app.include_router(admin)
app.include_router(products)
app.include_router(stock)
app.include_router(sale)


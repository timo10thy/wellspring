from fastapi import APIRouter, Depends, status
from app.models.users import User
from app.middlewares.admin import AdminOnly

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


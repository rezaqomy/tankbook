from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError, error_wrappers


from src.database.core import DbSession
from .service import create_user as service_create_user
from .models import User, UserRead, UserCreate



auth_router = APIRouter(prefix="/auth")
user_router = APIRouter(prefix="/user")



@user_router.post("/users/", response_model=UserRead)
async def create_user_view(user: UserCreate, db: DbSession):
    new_user = await service_create_user(user=user, db_session=db)
    return new_user

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError, error_wrappers


from src.database.core import DbSession
from .service import create
from .models import User, UserRead, UserCreate



auth_router = APIRouter(prefix="/auth")
user_router = APIRouter(prefix="/user")



@user_router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: DbSession):
    db_user = User(**user.dict(exclude={"password"}))
    db_user.set_password(user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

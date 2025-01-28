from fastapi import APIRouter, Depends, HTTPException, security, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED


from src.database.core import DbSession, get_db
from .service import (
    CurrentUser,
    get_by_username,
    create_user as service_create_user,
)
from .models import (
        User,
        UserRead,
        UserCreate,
        UserLogin,
        UserLoginResponse,
)


auth_router = APIRouter(prefix="/auth", tags=['auth'])
user_router = APIRouter(prefix="/user", tags=['user'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@user_router.post("/", response_model=UserRead)
async def create_user_view(user: UserCreate, db: DbSession):
    new_user = await service_create_user(user=user, db_session=db)
    return new_user



@auth_router.get("/me", response_model=UserRead)
async def get_me(
    user: CurrentUser,
):
    return user

    


@auth_router.post("/login", response_model=UserLoginResponse)
async def login_user(
    user_in: UserLogin,
    db_session: DbSession
):
    user = await get_by_username(db_session=db_session, username=user_in.username)
    if user and user.verify_password(user_in.password):
        return {"token": user.token}

    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=[
            {"loc": ["username"], "msg": "Invalid username.", "type": "value_error"},
            {"loc": ["password"], "msg": "Invalid password.", "type": "value_error"},
        ],
    )

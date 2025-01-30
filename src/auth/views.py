import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, security, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED


from src.database.core import DbSession, get_db
from .permissions import AdminPermission, any_permission
from .dependencies import admin_permission, current_user, current_user_or_admin
from .service import (
    CurrentUser,
    get_by_id,
    get_by_username,
    update_user as service_update_user,
    create_user as service_create_user,
)
from .models import (
        User,
        UserRead,
        UserCreate,
        UserLogin,
        UserLoginResponse,
        UserUpdate,
)


auth_router = APIRouter(prefix="/auth", tags=['auth'])
user_router = APIRouter(prefix="/user", tags=['user'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@user_router.post("/", response_model=UserRead)
async def create_user_view(user: UserCreate, db: DbSession):
    new_user = await service_create_user(user=user, db_session=db)
    return new_user



@user_router.patch("/{user_id}", 
                response_model=UserUpdate,
                dependencies=[Depends(current_user)]
            )
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: DbSession,
):
    user = await get_by_id(db_session=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    updated_user = await service_update_user(db_session=db, user=user, user_in=user_data)
    return updated_user
    
@user_router.get("/{user_id}", 
                response_model=UserRead,
                dependencies=[Depends(current_user_or_admin)]
                 )
async def get_user(
    user_id: int,
    db: DbSession,
):
    user = await get_by_id(db_session=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@user_router.get(
    "/", 
    response_model=List[UserRead],
    dependencies=[Depends(admin_permission)]
)
async def get_all_users(
    db: DbSession,
):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()

@user_router.delete("/{user_id}",
                dependencies=[Depends(admin_permission)]
            )
async def delete_user(
    user_id: int,
    db: DbSession,
):
    user = await get_by_id(db_session=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}


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
        token = user.token
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return {"token": token}

    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=[
            {"loc": ["username"], "msg": "Invalid username.", "type": "value_error"},
            {"loc": ["password"], "msg": "Invalid password.", "type": "value_error"},
        ],
    )

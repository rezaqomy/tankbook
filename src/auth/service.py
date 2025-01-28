from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import datetime, timedelta, UTC

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from src.database.core import DbSession, get_db
from .models import (UserCreate, User, TokenData)
from src.config import settings


JWT_EXP = settings.JWT_EXP
JWT_ALG = settings.JWT_ALG
JWT_SECRET = settings.JWT_SECRET


async def get_by_id(*, db_session: DbSession, id: int) -> Optional[User]:
    """return a user object based on user id"""
    stmt = select(User).where(User.id == id)
    result = await db_session.execute(stmt)
    return result.scalars().one_or_none()


async def get_by_email(*, db_session: DbSession, email: str) -> Optional[User]:
    """Returns a user object based on user email."""
    stmt = select(User).where(User.email == email)
    result = await db_session.execute(stmt)
    return result.scalars().one_or_none()



async def get_by_username(*, db_session: DbSession, username: str) -> Optional[User]:
    """Returns a user object based on user username."""
    stmt = select(User).where(User.username == username)
    result = await db_session.execute(stmt)
    return result.scalars().one_or_none()


async def get_by_phone_number(*, db_session: DbSession, phone_number: str) -> Optional[User]:
    """Returns a user object based on user phone number."""
    stmt = select(User).where(User.phone_number == phone_number)
    result = await db_session.execute(stmt)
    return result.scalars().one_or_none()


async def create_user(user: UserCreate, db_session: DbSession) -> Optional[User]:
    # Check if username already exists
    if await get_by_username(db_session=db_session, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )

    # Check if phone number already exists
    if await get_by_phone_number(db_session=db_session, phone_number=user.phone_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this phone number already exists.",
        )

    # Check if email already exists
    if await get_by_email(db_session=db_session, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    db_user = User(**user.dict(exclude={"password"}))
    db_user.set_password(user.password)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user



async def get_current_user(request: Request, db_session: AsyncSession = Depends(get_db)) -> User:
    """Attempts to get the current user using JWT token."""
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, 
            detail="Authorization header missing"
        )

    token = token.replace("Bearer ", "")
    print(token)
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    print(payload)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user = await get_by_username(db_session=db_session, username=username)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

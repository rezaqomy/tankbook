from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound


from src.database.core import DbSession
from .models import (UserCreate, User)
from src.enums import UserRoles



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

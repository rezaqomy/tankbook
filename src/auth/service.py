from .models import (UserCreate, User)
from src.enums import UserRoles


async def create(*, db_session, user_in: (UserCreate)) -> User:
    """Creates a new dispatch user."""
    # pydantic forces a string password, but we really want bytes
    password = bytes(user_in.password, "utf-8")

    # create the user
    user = User(
        **user_in.dict(exclude={"password", "organizations", "projects", "role"}), password=password
    )

    # add user to the current organization
    role = UserRoles.member
    if hasattr(user_in, "role"):
        role = user_in.role

    await db_session.add(user)
    await db_session.commit()
    return user

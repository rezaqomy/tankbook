from typing import Optional
from pydantic import EmailStr, validator, Field
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary, Boolean, DateTime


from src.database.core import Base
from src.models import TimeStampMixin, PrimaryKeyMixin, BookTankBase, PrimaryKey
from src.enums import UserRoles
from src.config import settings

from jose import jwt

from datetime import datetime, timedelta
import bcrypt


DISPATCH_JWT_EXP = settings.DISPATCH_JWT_EXP
DISPATCH_JWT_ALG = settings.DISPATCH_JWT_ALG
DISPATCH_JWT_SECRET = settings.DISPATCH_JWT_SECRET

def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class User(Base, TimeStampMixin, PrimaryKeyMixin):
    
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(String, default=UserRoles.CUSTOMER)


    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches stored hash"""
        if not password or not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def set_password(self, password: str) -> None:
        """Set a new password"""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = hash_password(password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=DISPATCH_JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "role": self.role,
        }
        return jwt.encode(data, DISPATCH_JWT_SECRET, algorithm=DISPATCH_JWT_ALG)



class UserBase(BookTankBase):
    username: str

    @validator("username")
    def username_required(cls, v):
        if not v:
            raise ValueError("Username is required")
        return v


class UserCreate(BookTankBase):
    username: str
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: str = Field(None, nullable=True)
    phone_number: str = Field(None, nullable=True)
    email: EmailStr = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True)

    @validator("password", pre=True)
    def hash(cls, v):
        return hash_password(str(v))


class UserRead(UserBase):
    id: PrimaryKey
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: Optional[str] = Field(default=None, nullable=True)
    username: str


from typing import Optional
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from pydantic import EmailStr, ValidationError, validator, Field
from sqlalchemy import Column, Float, ForeignKey, Integer, String, LargeBinary, Boolean, DateTime


from src.database.core import Base
from src.base import TimeStampMixin, PrimaryKeyMixin 
from src.schemas import BookTankBase, PrimaryKey


from src.enums import UserRoles
from src.config import EMAIL_REGEX, IRAN_PHONE_NUMBER_REGEX, settings

from jose import jwt

from datetime import UTC, datetime, timedelta
import bcrypt


JWT_EXP = settings.JWT_EXP
JWT_ALG = settings.JWT_ALG
JWT_SECRET = settings.JWT_SECRET



class User(Base, TimeStampMixin, PrimaryKeyMixin):
    
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    password = Column(LargeBinary, nullable=False)
    role = Column(String, default=UserRoles.CUSTOMER)
    exp = Column(Float, nullable=True)


    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches stored hash"""
        if not password or not self.password:
            return False
        result = bcrypt.checkpw(password.encode("utf-8"), self.password)
        return result

    def set_password(self, password: str) -> None:
        """Set a new password"""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password: str):
        """Generates a hashed version of the provided password."""
        pw = bytes(password, "utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pw, salt)


    @property
    def token(self):
        now = datetime.now(UTC)
        exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "id": self.id,
        }
        self.exp = exp
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)



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
    phone_number: str = Field(None, nullable=True, pattern=IRAN_PHONE_NUMBER_REGEX)
    email: EmailStr = Field(None, nullable=True, pattern=EMAIL_REGEX)
    password: Optional[str] = Field(None, nullable=True)

class UserUpdate(UserBase):
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: Optional[str] = Field(default=None, nullable=True)
    phone_number: Optional[str] = Field(default=None, nullable=True, pattern=IRAN_PHONE_NUMBER_REGEX)
    email: Optional[EmailStr] = Field(default=None, nullable=True, pattern=EMAIL_REGEX)
    exp: Optional[float] = Field(default=None, nullable=True)

class UserRead(UserBase):
    id: PrimaryKey
    username: str
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: Optional[str] = Field(default=None, nullable=True)
    phone_number: Optional[str] = Field(default=None, nullable=True)
    email: Optional[EmailStr] = Field(default=None, nullable=True)
    role: UserRoles
    exp: Optional[float] = Field(default=None, nullable=True)

class UserLogin(UserBase):
    password: str

    @validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


class UserLoginResponse(BookTankBase):
    token: Optional[str] = Field(None, nullable=True)


class UserRegister(UserLogin):
    password: Optional[str] = Field(None, nullable=True)

    @validator("password", pre=True, always=True)
    def password_required(cls, v):
        # we generate a password for those that don't have one
        if not v:
            raise ValueError("Must not be empty string")
        password = v 
        return User.hash_password(password)


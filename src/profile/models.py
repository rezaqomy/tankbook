from typing import Optional
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum
from datetime import datetime

from sqlalchemy.orm import relationship
from src.schemas import BookTankBase
from src.enums import SubscriptionModel
from src.auth.models import UserCreate, UserRead
from src.database.core import Base
from src.base import PrimaryKeyMixin



class Customer(Base):
    user = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    subscription_model = Column(Enum(SubscriptionModel), default=SubscriptionModel.FREE, nullable=False)
    subscription_end = Column(DateTime, nullable = True)
    wallet_money = Column(Integer, default=0, nullable=False)

class City(Base, PrimaryKeyMixin):
    name = Column(String, nullable=False)

class Author(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    city = Column(Integer, ForeignKey('city.id'))
    bank_number = Column(String(16), nullable=True)
    books = relationship("BookAuthor", back_populates="author")
    
class AuthorRegister(BookTankBase):
    user: UserCreate
    city: int
    bank_number: Optional[str]

class AuthorRead(BookTankBase):
    user_id: int
    city: int
    bank_number: Optional[str]

class CustomerRegister(BookTankBase):
    user: UserCreate
    

class CustomerGet(BookTankBase):
    user: int
    subscription_model: SubscriptionModel
    subscription_end: Optional[datetime]
    wallet_money: int

class CustomerRead(BookTankBase):
    user_id: int
    subscription_model: SubscriptionModel
    subscription_end: Optional[datetime] 
    wallet_money: int 

class CustomerUpdateResponse(BookTankBase):
    subscription_model: SubscriptionModel
    subscription_end: Optional[datetime]
    wallet_money: int

class CustomerUpdate(BookTankBase):
    subscription_model: Optional[SubscriptionModel] = None
    subscription_end: Optional[datetime] = None
    wallet_money: Optional[int] = None


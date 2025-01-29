from typing import Optional
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum
from datetime import datetime
from src.schemas import BookTankBase
from src.enums import SubscriptionModel
from src.auth.models import UserCreate, UserRead
from src.database.core import Base



class Customer(Base):
    user = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    subscription_model = Column(Enum(SubscriptionModel), default=SubscriptionModel.FREE, nullable=False)
    subscription_end = Column(DateTime, nullable = True)
    wallet_money = Column(Integer, default=0, nullable=False)


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


from pydantic import validator
from sqlalchemy import Column, DateTime, ForeignKey, Integer, null
from src.database.core import Base
from src.schemas import BookTankBase
from src.base import PrimaryKeyMixin, TimeStampMixin
from datetime import datetime

class Reserve(Base, PrimaryKeyMixin, TimeStampMixin):
    customer_id = Column(Integer, ForeignKey('customer.user'), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

class ReserveBase(BookTankBase):
    customer_id: int
    book_id: int
    start: datetime
    end: datetime
    price: int

    @validator("start", "end", pre=True)
    def parse_and_make_naive(cls, v):
        if isinstance(v, str):  # Convert string to datetime if necessary
            v = datetime.fromisoformat(v)
        return v.replace(tzinfo=None) if v.tzinfo else v
class ReserveCreate(ReserveBase):
    pass

class ReserveUpdate(ReserveBase):
    pass

class ReserveResponse(ReserveBase):
    id: int

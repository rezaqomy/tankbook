

from typing import Optional, Any, List
from pydantic import Field
from pydantic.utils import GetterDict
from sqlalchemy import Column, ForeignKey, Integer, String, null
from sqlalchemy.orm import relationship
from sqlalchemy.util import FastIntFlag
from src.base import PrimaryKeyMixin, TimeStampMixin
from src.schemas import BookTankBase
from src.database.core import Base
from sqlalchemy.ext.associationproxy import association_proxy

class BookAuthor(Base):
    book_id = Column(ForeignKey('book.id'), primary_key=True)
    author_id = Column(ForeignKey('author.user_id'), primary_key=True)
    blurb = Column(String, nullable=False)
    book = relationship("Book", back_populates="authors")
    author = relationship("Author", back_populates="books")

    author_name = association_proxy(target_collection='author', attr='name')
    book_title = association_proxy(target_collection='book', attr='title')

class Gener(Base, PrimaryKeyMixin):
    name = Column(String, nullable=False)

class Book(Base, PrimaryKeyMixin, TimeStampMixin):
    title = Column(String(255), nullable=False)
    isbn = Column(String(13), nullable=False, unique=True)
    price = Column(Integer, nullable=False, default=0)
    gener = Column(Integer, ForeignKey('gener.id'), nullable=False)
    description = Column(String(2056), nullable=True)
    unit = Column(Integer, default=0, nullable=False)

    authors = relationship("BookAuthor", back_populates="book")

class BookCreateSchema(BookTankBase):
    title: str = Field(..., max_length=255)
    isbn: str = Field(..., max_length=13)
    price: int = Field(..., ge=0)
    gener: int
    description: Optional[str] = Field(None, max_length=2056)
    unit: int = Field(0, ge=0)
    author_ids: List[int]
    blurbs: List[str]

class AuthorResponse(BookTankBase):
    user_id: int
    city: Optional[int]
    bank_number: Optional[str]

    class Config:
        orm_mode = True

class BookAuthorResponse(BookTankBase):
    author: AuthorResponse
    blurb: str
    book_title: str

    class Config:
        orm_mode = True

class BookResponse(BookTankBase):
    id: int
    title: str
    isbn: str
    price: int
    gener: int
    description: Optional[str]
    unit: int
    authors: List[BookAuthorResponse]

class UpdateBookSchema(BookCreateSchema):
    title: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[int] = None
    gener: Optional[int] = None
    description: Optional[str] = None
    unit: Optional[int] = None
    author_ids: Optional[List[int]] = None
    blurbs: Optional[List[str]] = None

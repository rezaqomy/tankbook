

from sqlalchemy import Column, ForeignKey, Integer, String, null
from sqlalchemy.orm import relationship
from sqlalchemy.util import FastIntFlag
from src.base import PrimaryKeyMixin, TimeStampMixin
from src.database.core import Base


class BookAuthor(Base, PrimaryKeyMixin):
    book_id = Column(ForeignKey('book.id'), primary_key=True)
    author_id = Column(ForeignKey('author.user_id'), primary_key=True)
    blurb = Column(String, nullable=False)
    book = relationship("Book", back_populates="author")
    author = relationship("Author", back_populates="book")

class Gener(Base, PrimaryKeyMixin):
    name = Column(String, nullable=False)

class Book(Base, PrimaryKeyMixin, TimeStampMixin):
    title = Column(String(255), nullable=False)
    isbn = Column(String(13), nullable=False, unique=True)
    price = Column(Integer, nullable=False, default=0)
    description = Column(String(2056), nullable=True)
    unit = Column(Integer, default=0)
    authors = relationship("BookAuthor", back_populates="book")

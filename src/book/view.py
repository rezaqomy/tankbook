from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .service import BookService
from src.database.core import DbSession
from .models import Book, BookCreateSchema, BookResponse


book_router = APIRouter(prefix="/book", tags=["book"])

@book_router.post("/", response_model=BookResponse) 
async def create_book(book_data: BookCreateSchema, db: DbSession):
    book = await BookService.create_book(db, book_data, book_data.author_ids, book_data.blurbs)
    return book


@book_router.get("/{id}", response_model=BookResponse)
async def get_book(id: int, db: DbSession):
    result = await db.execute(select(Book).options(joinedload(Book.authors)).filter(Book.id == id))
    db_book = result.scalars().first()  # Use scalars().first() instead of scalar_one_or_none()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_book

@book_router.get("/", response_model=List[BookResponse])
async def get_books(db: DbSession):
    result = await db.execute(select(Book).options(joinedload(Book.authors)))
    db_books = result.scalars().all()  # Get all records (books)
    return db_books

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.auth.service import CurrentUser
from src.auth.dependencies import admin_permission, author_or_admin_permissasion

from .service import BookService, get_by_isbn
from src.database.core import DbSession
from src.enums import UserRoles
from .models import Book, BookCreateSchema, BookResponse, UpdateBookSchema


book_router = APIRouter(prefix="/book", tags=["book"])

@book_router.post("/", response_model=BookResponse, dependencies=[Depends(author_or_admin_permissasion)]) 
async def create_book(book_data: BookCreateSchema, db: DbSession, user: CurrentUser):
    if user.role == UserRoles.AUTHOR:
        book_data.author_ids = [user.id]
        book_data.blurbs = [user.first_name]
    book = await BookService.create_book(db, book_data, book_data.author_ids, book_data.blurbs)
    return book
@book_router.get("/{id}", response_model=BookResponse)
async def get_book(id: int, db: DbSession):
    db_book = await BookService.get_book(db, id)
    return db_book

@book_router.get("/", response_model=List[BookResponse])
async def get_books(db: DbSession):
    db_books = await BookService.get_all_books(db)
    return db_books

@book_router.put("/{id}", response_model=BookResponse)
async def update_book(id: int, book_data: UpdateBookSchema, db: DbSession):
    updated_book = await BookService.update_book(db, id, book_data)
    return updated_book

@book_router.delete("/{id}", response_model=dict)
async def delete_book(id: int, db: DbSession):
    response = await BookService.delete_book(db, id)
    return response

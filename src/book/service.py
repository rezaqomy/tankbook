from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from .models import Book, BookAuthor, BookCreateSchema
from src.profile.models import Author
from src.database.core import DbSession


async def create_book_author(*, db: DbSession, book_id: int, author_id: int, blurb: str):
    book_author = BookAuthor(book_id=book_id, author_id=author_id, blurb=blurb)
    db.add(book_author)
    await db.commit()
    await db.refresh(book_author)
    return book_author


async def get_by_isbn(*, db_session: DbSession, isbn: str):
    result = await db_session.execute(select(Book).filter(Book.isbn == isbn))
    return result.scalar_one_or_none()


class BookService:
    
    @staticmethod
    async def create_book(db: DbSession, book_data: BookCreateSchema, author_ids: List[int], blurbs: List[str]):
        if await get_by_isbn(db_session=db, isbn=book_data.isbn):
            raise HTTPException(status_code=400, detail=f"Book with ISBN {book_data.isbn} already exists")

        if len(author_ids) != len(blurbs):
            raise HTTPException(status_code=400, detail="Each author must have a corresponding blurb")

        book = Book(**book_data.model_dump(exclude={'author_ids', 'blurbs'}))
        db.add(book)
        await db.commit()
        await db.refresh(book)

        # Preload all authors in one query to avoid repeated DB calls
        authors = await db.execute(select(Author).where(Author.user_id.in_(author_ids)))
        author_dict = {author.user_id: author for author in authors.scalars().all()}


        book_authors = []
        for author_id, blurb in zip(author_ids, blurbs):
            author = author_dict.get(author_id)
            if not author:
                raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")

            book_authors.append(BookAuthor(book_id=book.id, author_id=author_id, blurb=blurb))

        db.add_all(book_authors)
        await db.commit()

        return book

from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from .models import Book, BookAuthor, BookCreateSchema, UpdateBookSchema
from src.profile.models import Author
from src.database.core import DbSession


async def create_book_author(*, db: DbSession, book_id: int, author_id: int, blurb: str) -> BookAuthor:
    book_author = BookAuthor(book_id=book_id, author_id=author_id, blurb=blurb)
    db.add(book_author)
    await db.commit()
    await db.refresh(book_author)
    return book_author


async def get_by_isbn(*, db_session: DbSession, isbn: str) -> Book | None:
    result = await db_session.execute(select(Book).filter(Book.isbn == isbn))
    return result.scalar_one_or_none()


class BookService:
    
    @staticmethod
    async def create_book(db: DbSession, book_data: BookCreateSchema, author_ids: List[int], blurbs: List[str]):
        # Check if ISBN is already taken
        if await get_by_isbn(db_session=db, isbn=book_data.isbn):
            raise HTTPException(status_code=400, detail=f"Book with ISBN {book_data.isbn} already exists")

        # Ensure each author has a matching blurb
        if len(author_ids) != len(blurbs):
            raise HTTPException(status_code=400, detail="Each author must have a corresponding blurb")

        # Create the Book instance
        book = Book(**book_data.model_dump(exclude={'author_ids', 'blurbs'}))
        db.add(book)
        await db.commit()
        await db.refresh(book)

        # Preload all authors in a single query
        authors = await db.execute(select(Author).where(Author.user_id.in_(author_ids)))
        author_dict = {author.user_id: author for author in authors.scalars().all()}

        # Create BookAuthor records
        book_authors = []
        for author_id, blurb in zip(author_ids, blurbs):
            author = author_dict.get(author_id)
            if not author:
                raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
            book_authors.append(BookAuthor(book_id=book.id, author_id=author_id, blurb=blurb))

        db.add_all(book_authors)
        await db.commit()

        # Eagerly load the Book again with authors to avoid lazy-loading issues
        result = await db.execute(
            select(Book)
            .options(selectinload(Book.authors).selectinload(BookAuthor.author))
            .filter(Book.id == book.id)
        )
        book_loaded = result.scalars().first()
        return book_loaded

    @staticmethod
    async def get_all_books(db: DbSession):
        result = await db.execute(select(Book).options(selectinload(Book.authors).selectinload(BookAuthor.author)))
        return result.scalars().all()

    @staticmethod
    async def get_book(db: DbSession, book_id: int):
        result = await db.execute(
            select(Book)
            .options(selectinload(Book.authors).selectinload(BookAuthor.author))
            .filter(Book.id == book_id)
        )
        book = result.scalars().first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    @staticmethod
    async def update_book(db: DbSession, book_id: int, book_data: UpdateBookSchema):
        result = await db.execute(
            select(Book).options(selectinload(Book.authors)).filter(Book.id == book_id)
        )
        book = result.scalars().first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Check if new ISBN is unique
        if book_data.isbn:
            existing_book = await db.execute(select(Book).filter(Book.isbn == book_data.isbn, Book.id != book_id))
            if existing_book.scalars().first():
                raise HTTPException(status_code=400, detail="ISBN must be unique")

        # Update fields if provided
        for field, value in book_data.model_dump(exclude_unset=True).items():
            setattr(book, field, value)
        
        await db.commit()
        await db.refresh(book)


        if book_data.author_ids is not None:
            await db.execute(delete(BookAuthor).where(BookAuthor.book_id == book_id))
            await db.commit()

        # Update authors if provided
        if book_data.author_ids and book_data.blurbs:
            if len(book_data.author_ids) != len(book_data.blurbs):
                raise HTTPException(status_code=400, detail="Each author must have a corresponding blurb")

            # Add new author relationships
            for author_id, blurb in zip(book_data.author_ids, book_data.blurbs):
                book_author = BookAuthor(book_id=book_id, author_id=author_id, blurb=blurb)
                db.add(book_author)

            await db.commit()
            await db.flush()
        result = await db.execute(
            select(Book)
            .options(selectinload(Book.authors).selectinload(BookAuthor.author))
            .filter(Book.id == book.id)
        )
        book_loaded = result.scalars().first()
        return book_loaded
    
    @staticmethod
    async def delete_book(db: DbSession, book_id: int):
        # First, fetch the book to ensure it exists
        result = await db.execute(select(Book).filter(Book.id == book_id))
        book = result.scalars().first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Delete related BookAuthor entries
        await db.execute(delete(BookAuthor).where(BookAuthor.book_id == book_id))
        await db.commit()

        # Now delete the book itself
        await db.execute(delete(Book).where(Book.id == book_id))
        await db.commit()

        return {"detail": "Book deleted successfully"}

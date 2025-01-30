
from fastapi import HTTPException
from src.database.core import DbSession
from src.profile.service import CustomerService
from src.book.service import BookService
from .models import ReserveCreate, Reserve, ReserveUpdate


class ReserveService:
    @staticmethod
    async def create_reserve(db: DbSession, reserve_data: ReserveCreate) -> Reserve:
        if await CustomerService.get_customer(db_session=db, user_id=reserve_data.customer_id) is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        if await BookService.get_book(db, reserve_data.book_id) is None:
            raise HTTPException(status_code=404, detail="Book not found")


        reserve = Reserve(**reserve_data.dict())
        db.add(reserve)
        await db.commit()
        await db.refresh(reserve)
        return reserve

    @staticmethod
    async def get_reserve(db: DbSession, reserve_id: int) -> Reserve:
        reserve = await db.get(Reserve, reserve_id)
        if not reserve:
            raise HTTPException(status_code=404, detail="Reserve not found")
        return reserve

    @staticmethod
    async def update_reserve(db: DbSession, reserve_id: int, reserve_data: ReserveUpdate) -> Reserve:
        reserve = await db.get(Reserve, reserve_id)
        if reserve:
            if reserve_data.customer_id is not None and await CustomerService.get_customer(db_session=db, user_id=reserve_data.customer_id) is None:
                raise HTTPException(status_code=404, detail="Customer not found")

            if reserve_data.book_id is not None and await BookService.get_book(db, reserve_data.book_id) is None:
                raise HTTPException(status_code=404, detail="Book not found")

            for key, value in reserve_data.dict().items():
                setattr(reserve, key, value)
            await db.commit()
            await db.refresh(reserve)
        return reserve

    @staticmethod
    async def delete_reserve(db: DbSession, reserve_id: int) -> None:
        reserve = await db.get(Reserve, reserve_id)
        if reserve:
            await db.delete(reserve)
            await db.commit()


from datetime import UTC
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import delete
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_404_NOT_FOUND
from src.reserve.models import Reserve
from src.enums import SubscriptionModel, UserRoles
from src.database.core import DbSession
from src.auth.service import create_user
from .models import City, Customer, CustomerRegister, CustomerUpdate, AuthorRegister, Author


class CityService:
    @staticmethod
    async def get_city(*, city_id: int, db_session: DbSession) -> City | None:
        city = await db_session.get(City, city_id)
        if not city:
            raise HTTPException(HTTP_404_NOT_FOUND, detail=f"The city with id {city_id} not found!")
        return city


class AuthorService:
    @staticmethod
    async def create(*, author: AuthorRegister, db_session: DbSession) -> Author:
        if await CityService.get_city(city_id=author.city, db_session=db_session) is None:
            raise HTTPException(HTTP_404_NOT_FOUND, detail=f"The city with id {author.city} not found!")

        user = await create_user(user=author.user, db_session=db_session, role=UserRoles.AUTHOR)
        author_db = Author(user_id=user.id, city=author.city, bank_number=author.bank_number)
        db_session.add(author_db)
        await db_session.commit()
        await db_session.refresh(author_db)
        return author_db


class CustomerService:
    @staticmethod
    async def create(*, customer: CustomerRegister, db_session: DbSession) -> Customer:
        user = await create_user(user=customer.user, db_session=db_session)
        customer_db = Customer(user=user.id)
        db_session.add(customer_db)
        await db_session.commit()
        await db_session.refresh(customer_db)
        return customer_db

    @staticmethod
    async def update(*, user_id: int, customer_update: CustomerUpdate, db_session: DbSession) -> Customer:
        customer = await db_session.get(Customer, user_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        update_data = customer_update.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(customer, key, value)

        await db_session.commit()
        await db_session.refresh(customer)

        return customer
    
    @staticmethod
    async def get_customer(*, user_id: int, db_session: DbSession) -> Customer:
        customer = await db_session.get(Customer, user_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    
    

    @staticmethod
    async def delete_customer(db_session: DbSession, user_id: int):
        try:
            # Check if the customer has any reservations
            result = await db_session.execute(select(Reserve).where(Reserve.customer_id == user_id))
            reservations = result.scalars().all()

            if reservations:
                raise HTTPException(status_code=400, detail="Cannot delete customer with active reservations.")

            customer = await db_session.get(Customer, user_id)
            if customer:
                await db_session.delete(customer)
                await db_session.commit()
                return {"message": "Customer deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Customer not found")

        except IntegrityError:
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Cannot delete customer as they have linked reservations.")

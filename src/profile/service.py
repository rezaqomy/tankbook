
from datetime import UTC
from fastapi import HTTPException
from src.enums import SubscriptionModel
from src.database.core import DbSession
from src.auth.service import create_user
from .models import Customer, CustomerRegister, CustomerUpdate

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

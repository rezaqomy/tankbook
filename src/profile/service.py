
from src.enums import SubscriptionModel
from src.database.core import DbSession
from src.auth.service import create_user
from .models import Customer, CustomerRegister

class CustomerService:
    @staticmethod
    async def create(*, customer: CustomerRegister, db_session: DbSession) -> Customer:
        user = await create_user(user=customer.user, db_session=db_session)
        customer_db = Customer(user=user.id)
        db_session.add(customer_db)
        await db_session.commit()
        await db_session.refresh(customer_db)
        return customer_db




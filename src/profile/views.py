from fastapi import APIRouter

from src.auth.models import UserRead
from src.auth.service import get_by_id
from src.database.core import DbSession
from .models import CustomerRead, CustomerRegister
from .service import CustomerService


profile_route = APIRouter(prefix="/profile", tags=["profile", "customer"])


@profile_route.post('/customer', response_model=CustomerRead)
async def create_customer_view(
    customer: CustomerRegister,
    db_session: DbSession,
    ):
    new_customer = await CustomerService.create(customer=customer, db_session=db_session)
    return {
        "user_id": new_customer.user,
        "subscription_model": new_customer.subscription_model,
        "subscription_end": new_customer.subscription_end,
        "wallet_money": new_customer.wallet_money
    }

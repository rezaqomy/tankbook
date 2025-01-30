from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql import select

from src.auth import dependencies
from src.auth.dependencies import admin_permission, current_user_or_admin
from src.auth.permissions import AdminPermission
from src.database.core import DbSession
from .models import AuthorRead, AuthorRegister, CustomerGet, CustomerRead, CustomerRegister, CustomerUpdate, Customer, CustomerUpdateResponse
from .service import AuthorService, CustomerService


profile_route = APIRouter(prefix="/profile", tags=["profile"])


@profile_route.get("/customers", response_model=List[CustomerGet], dependencies=[Depends(admin_permission)])
async def get_all_customers(db: DbSession):
    # Asynchronous query
    result = await db.execute(select(Customer))
    customers = result.scalars().all()
    return customers

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

@profile_route.get("/customer/{user_id}", response_model=CustomerGet, dependencies=[Depends(current_user_or_admin)])
async def get_one_customer(user_id: int, db: DbSession):
    # Asynchronous query to get a single customer
    result = await db.execute(select(Customer).filter(Customer.user == user_id))
    customer = result.scalars().first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer



@profile_route.patch('/customer/{user_id}', response_model=CustomerUpdateResponse, dependencies=[Depends(admin_permission)])
async def update_customer_view(
    user_id: int,
    customer_update: CustomerUpdate,
    db_session: DbSession,
):
    customer = await db_session.get(Customer, user_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)

    await db_session.commit()
    await db_session.refresh(customer)

    return customer


@profile_route.delete("/customer/{user_id}", status_code=204 , dependencies=[Depends(admin_permission)])
async def delete_customer_view(
    user_id: int,
    db_session: DbSession,
):
    await CustomerService.delete_customer(user_id=user_id, db_session=db_session)
    return None


@profile_route.post('/author', response_model=AuthorRead)
async def create_author_view(author: AuthorRegister, db_session: DbSession):
    new_author = await AuthorService.create(author=author, db_session=db_session)
    return new_author

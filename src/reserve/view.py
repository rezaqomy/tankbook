from fastapi import APIRouter 
from src.database.core import DbSession
from .models import ReserveCreate, ReserveUpdate, ReserveResponse
from .service import ReserveService

reserve_router = APIRouter(prefix="/reserves", tags=["reserves"])

@reserve_router.post("/", response_model=ReserveResponse)
async def create_reserve(reserve_data: ReserveCreate, db: DbSession):
    return await ReserveService.create_reserve(db, reserve_data)

@reserve_router.get("/{reserve_id}", response_model=ReserveResponse)
async def get_reserve(reserve_id: int, db: DbSession):
    return await ReserveService.get_reserve(db, reserve_id)

@reserve_router.put("/{reserve_id}", response_model=ReserveResponse)
async def update_reserve(reserve_id: int, reserve_data: ReserveUpdate, db: DbSession):
    return await ReserveService.update_reserve(db, reserve_id, reserve_data)

@reserve_router.delete("/{reserve_id}")
async def delete_reserve(reserve_id: int, db: DbSession):
    await ReserveService.delete_reserve(db, reserve_id)
    return {"message": "Reserve deleted successfully"}

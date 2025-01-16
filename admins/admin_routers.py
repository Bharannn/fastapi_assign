from fastapi import APIRouter, Depends
from utils import admin_access
from admins.admin_operations import fetch_all_users, fetch_all_orders

admin_routers = APIRouter(prefix="/admin", tags=["Admin"])

@admin_routers.get("/users", dependencies=[Depends(admin_access)])
async def get_all_users():
    return await fetch_all_users()


@admin_routers.get("/orders", dependencies=[Depends(admin_access)])
async def get_all_orders():
    return await fetch_all_orders()

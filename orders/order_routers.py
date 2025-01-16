from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from orders.order_validations import (
    OrderCreate
    )
from orders.order_operations import (
    create_order_logic, get_user_orders_logic, get_order_by_id_logic
    )
from utils import user_access
from utils import limiter

order_routers = APIRouter(prefix="/orders", tags=["Order Management"])

# Route to create an order
@order_routers.post("/", summary="Create a new order")
@limiter.limit("5/hour")  # Allow only 5 requests per hour per user
async def create_order(request: Request, order: OrderCreate, current_user: dict = Depends(user_access)):
    try:
        result = await create_order_logic(order, current_user)
        return {"message": "Order created successfully", "order": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to get all orders for the logged-in user
@order_routers.get("/", summary="Get all orders for the logged-in user")
async def get_user_orders(request: Request, current_user: dict = Depends(user_access)):
    try:
        return await get_user_orders_logic(current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to get a specific order by its ID
@order_routers.get("/{order_id}", summary="Get order by ID")
async def get_order_by_id(request: Request, order_id: str, current_user: dict = Depends(user_access)):
    try:
        result = await get_order_by_id_logic(order_id, current_user)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
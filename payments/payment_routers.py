from fastapi import APIRouter, Request
from payments.payment_operations import create_checkout_session, handle_webhook

payment_routers = APIRouter(prefix="/payments", tags=["Payments"])

@payment_routers.post("/checkout/{order_id}", summary="Initiate Payment")
async def checkout(order_id: str):
    return await create_checkout_session(order_id)

@payment_routers.post("/webhook", summary="Handle Payment Webhook")
async def webhook(request: Request):
    return await handle_webhook(request)

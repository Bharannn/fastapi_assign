import stripe
from fastapi import HTTPException, Request
from database import Orders

stripe.api_key = "sk_test_51QcMPQC2tGgtjV9YYJjH9AUScmTxY27wALfaNztM9IZQDCWwZEfO0mEUn0AeIBBLUOVcqt2wtHTh2XPDD8ST240T00XnU0kL6N"

async def create_checkout_session(order_id: str):
    # Fetch order details
    order = Orders.objects(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Order #{order.id}",
                    },
                    "unit_amount": int(order.total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/payments/success",
        cancel_url="http://localhost:8000/payments/cancel",
    )
    return {"checkout_url": session.url}


async def handle_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = "your_webhook_secret"

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["client_reference_id"]
        order = Orders.objects(id=order_id).first()
        if order:
            order.payment_status = "paid"
            order.order_status = "confirmed"
            order.save()
    return {"status": "success"}

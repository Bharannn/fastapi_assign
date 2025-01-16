from fastapi.middleware.cors import CORSMiddleware
from config import settings
from fastapi import FastAPI, HTTPException, Request

from users.user_routers import user_routers
from orders.order_routers import order_routers
from admins.admin_routers import admin_routers
from payments.payment_routers import payment_routers
from utils import limiter, rate_limit_exceeded_handler


app = FastAPI()
app.state.limiter = limiter

app.add_exception_handler(429, rate_limit_exceeded_handler)

origins = [
    settings.CLIENT_ORIGIN,
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Login Operations
app.include_router(user_routers)
app.include_router(order_routers)
app.include_router(admin_routers)
app.include_router(payment_routers)


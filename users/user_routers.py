# users/user_routers.py
from fastapi import BackgroundTasks, APIRouter, Depends
from fastapi.responses import JSONResponse

from users.user_validations import UserRegister, UserLogin, UserUpdate
from users.user_operations import (
    verify_email, register_user,
    login_user, get_profile,
    update_profile
)
from utils import user_access


user_routers = APIRouter(
    prefix='/user',
    tags=['User management']
)

@user_routers.get("/verify-email")
async def verify_email_endpoint(token: str):
    result = await verify_email(token)
    return JSONResponse(content=result)

@user_routers.post("/register")
async def register_user_endpoint(user: UserRegister, background_tasks: BackgroundTasks):
    result = await register_user(user, background_tasks)
    return JSONResponse(content=result)

@user_routers.post("/login")
async def login_user_endpoint(user: UserLogin):
    result = await login_user(user)
    return JSONResponse(content=result)

@user_routers.get("/profile")
async def get_profile_endpoint(current_user: dict = Depends(user_access)):
    result = await get_profile(current_user)
    return JSONResponse(content=result)

@user_routers.put("/profile")
async def update_profile_endpoint(updated_data: UserUpdate, current_user: dict = Depends(user_access)):
    result = await update_profile(updated_data, current_user)
    return JSONResponse(content=result)

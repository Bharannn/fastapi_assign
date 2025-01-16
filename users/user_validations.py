# users/user_validations.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re


class UserProfile(BaseModel):
    id : str
    username: str
    email: str
    created_at : str

class UserRegister(BaseModel):
    # id : Optional[str]
    role_id: str
    username: str
    email: str
    password: str
    # time_stamp : str

    @validator("email")
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        return value

class UserLogin(BaseModel):
    username: str
    password: str

class RoleId(BaseModel):
    id : str
    role_name : str

class AuthDetails(BaseModel):
    id : str
    # email : EmailStr
    password : str
    verified : bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    @validator("email")
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        return value

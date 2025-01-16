#utils.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from config import settings
from database import User


limiter = Limiter(key_func=get_remote_address)
rate_limit_exceeded_handler= _rate_limit_exceeded_handler

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# PRIVATE_KEY = (
#     "-----BEGIN RSA PRIVATE KEY-----"
#     + settings.JWT_PRIVATE_KEY
#     + "-----END RSA PRIVATE KEY-----"
# )

# PUBLIC_KEY = (
#     "-----BEGIN RSA PUBLIC KEY-----"
#     + settings.JWT_PUBLIC_KEY
#     + "-----END RSA PUBLIC KEY-----"
# )

# PRIVATE_KEY = f"""-----BEGIN RSA PRIVATE KEY-----
# {settings.JWT_PRIVATE_KEY}
# -----END RSA PRIVATE KEY-----"""

# PUBLIC_KEY = f"""-----BEGIN PUBLIC KEY-----
# {settings.JWT_PUBLIC_KEY}
# -----END PUBLIC KEY-----"""


PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIBOAIBAAJAW+QMKv4apiMa/I+HvvwLOcUHd9azYC1JU1kIUT21w2CsIttZxJi7
oKAOs3soSpPpPyh8omqXsOZLlKIbvgwCrQIDAQABAkBbzLdbO//jea68Iae7ZJDS
ZcPQNO1+Z7+ZRJjKkJvFUtunvuoOvAESqzrQs6LaOZcWTRvhytbzdlBUmwULfukB
AiEAorvvn5veYOJYfKg/1IZ8mARAqrdTmHquJh9G9SzgdD8CIQCQjhr0KZSBeUoF
LBUWpvOW/HQCyGeansUE4ksI4zweEwIgbvgdFQfjAsoWcRsCO9hhigAMYN2WgbnW
m2RkrLenb10CIH871RWbk47yhuhOiLFLeZQn2KSqaCZ8IMXPuGO2Pq/pAiBS0ibz
I9wWf6+xuXbYXmZFE8i19LEl8Q1UQS8WsjMytQ==
-----END RSA PRIVATE KEY-----
"""

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MFswDQYJKoZIhvcNAQEBBQADSgAwRwJAW+QMKv4apiMa/I+HvvwLOcUHd9azYC1J
U1kIUT21w2CsIttZxJi7oKAOs3soSpPpPyh8omqXsOZLlKIbvgwCrQIDAQAB
-----END PUBLIC KEY-----
"""

# print(PRIVATE_KEY)

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
    return payload

def user_access(Token: str):
    if not Token:
        raise HTTPException(status_code=400, detail="Token is missing.")
    try:
        # Extract the token part from 'Bearer <token>'
        token = Token
        payload = verify_token(token)
        user = User.objects(id=payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_dict = {
            "id": str(user.id),  # Convert ObjectId to string for JSON serialization
            "username": user.username,
            "email": user.email,
            "role": user.role_id.role_name,
        }
        return user_dict
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except IndexError:
        raise HTTPException(status_code=400, detail="Malformed Authorization header")

    
def admin_access(Token: str):
    if not Token:
        raise HTTPException(status_code=400, detail="Token is missing.")

    try:
        # Extract the token part from 'Bearer <token>'
        token = Token
        payload = verify_token(token)

        # Fetch the user using the `id` from the token payload
        user = User.objects(id=payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check the user's role
        if not user.role_id or user.role_id.role_name != "Admin":
            raise HTTPException(status_code=403, detail="Admin access required")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except IndexError:
        raise HTTPException(status_code=400, detail="Malformed Authorization header")

  

# Mail Configuration
conf = ConnectionConfig(
    MAIL_USERNAME = settings.EMAIL_USERNAME,
    MAIL_PASSWORD = settings.EMAIL_PASSWORD,
    MAIL_FROM = settings.EMAIL_FROM,
    MAIL_PORT = settings.EMAIL_PORT,
    MAIL_SERVER = settings.EMAIL_HOST,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
    
# Utility function to send an email
async def send_verification_email(email: str, token: str, background_tasks: BackgroundTasks):
    verification_link = f"http://127.0.0.1:8000/user/verify-email?token={token}"  # Include the token in the query
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <p>Click the link below to verify your email:</p>
                <a href="{verification_link}">Verify Email</a>
            </body>
        </html>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

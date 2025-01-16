# users/user_operations.py
from fastapi import BackgroundTasks, HTTPException, Depends
from datetime import datetime
from users.user_validations import (
    UserRegister, UserLogin,AuthDetails, UserUpdate
)
from utils import (
    hash_password, verify_password,
    create_access_token, verify_token,
    send_verification_email
)
from database import User, Roles, AuthDetails


# Verify Email
async def verify_email(token: str):
    try:
        # Decode the token to extract user information
        payload = verify_token(token)
        user_id = payload["sub"]

        # Update the `verified` flag in the database
        auth_details = AuthDetails.objects(id=user_id).first()
        if not auth_details:
            raise HTTPException(status_code=404, detail="User not found")
        
        auth_details.verified = True
        auth_details.save()

        # Provide a user-friendly response
        return {
            "message": "Email successfully verified. You can now log in.",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Register User
async def register_user(user: UserRegister, background_tasks: BackgroundTasks):
    # Check if email already exists
    if User.objects(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # # Check if role exists
    role = Roles.objects(id=user.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role ID")

    # Hash the password and create user entry
    hashed_password = hash_password(user.password)
    new_user = User(
        role_id=role,
        username=user.username,
        email=user.email,
        time_stamp=datetime.utcnow()
    )
    new_user.save()

    # Create AuthDetails entry for the user
    auth_details = AuthDetails(
        id=new_user,
        password=hashed_password,
        verified=False
    )
    auth_details.save()

    # Generate a token for email verification
    token_data = {"sub": new_user.id, 
                  "role": role.role_name}
    verification_token = create_access_token(token_data)

    # Send verification email asynchronously
    background_tasks.add_task(send_verification_email, user.email, verification_token, background_tasks)

    return {"message": "User registered successfully. Please verify your email to activate your account."}


# Login User
async def login_user(user: UserLogin):
    db_user = User.objects(username=user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    auth_details = AuthDetails.objects(id=db_user).first()
    if not auth_details or not verify_password(user.password, auth_details.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not auth_details.verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please check your email.")

    token_data = {"sub": db_user.id, "role": db_user.role_id.role_name}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


# Get Profile
async def get_profile(current_user: dict):
    user = User.objects(id=current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile_data = {
        "_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role_id.role_name,
        "time_stamp": user.time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
        "status": user.status
    }
    return profile_data


async def update_profile(updated_data: UserUpdate, current_user: dict):
    # Retrieve the user object from the database
    user = User.objects(id=current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Extract fields to be updated
    update_dict = updated_data.dict(exclude_unset=True)

    # Update the username if provided
    if "username" in update_dict:
        user.username = update_dict["username"]

    # Update the email if provided and validate uniqueness
    if "email" in update_dict and update_dict["email"] != user.email:
        if User.objects(email=update_dict["email"]).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = update_dict["email"]

    # Update the password if provided
    if "password" in update_dict:
        auth_details = AuthDetails.objects(id=user).first()
        if not auth_details:
            raise HTTPException(status_code=404, detail="User authentication details not found")
        auth_details.password = hash_password(update_dict["password"])
        auth_details.save()

    # Save the updated user object
    user.save()

    return {"message": "Profile updated successfully"}

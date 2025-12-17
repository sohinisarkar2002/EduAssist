from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.crud import get_user_by_email, hash_password, verify_password
from app.models import User
from app.database import get_db
from app.auth.jwt import create_access_token
from app.services.email_service import send_email_async
from datetime import datetime, timedelta
import secrets
import os
from app.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
# Registration
@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check user exists...
    new_user = User(email=user.email, username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
# Login
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
# Request Password Reset
@router.post("/password-reset-request")
async def password_reset_request(email: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=2)
    user.password_reset_token = token
    user.password_reset_expiry = expiry
    await db.commit()
    reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
    subject = "EduAssist Password Reset"
    html = f"<p>Click here to reset your password: <a href='{reset_link}'>{reset_link}</a></p>"
    background_tasks.add_task(send_email_async, user.email, subject, html)
    return {"msg": "Password reset link sent."}
# Password Reset
@router.post("/reset-password")
async def password_reset(token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.password_reset_token == token))
    user = user.scalar_one_or_none()
    if not user or user.password_reset_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired or invalid.")
    user.hashed_password = hash_password(new_password)
    user.password_reset_token = None
    user.password_reset_expiry = None
    await db.commit()
    return {"msg": "Password updated."}

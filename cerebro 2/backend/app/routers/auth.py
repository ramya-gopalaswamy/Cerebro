"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Optional
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.storage.user_db import user_db
import jwt
from datetime import datetime, timedelta
from fastapi import Request

router = APIRouter()

SECRET_KEY = "your_secret_key_here"  # Replace with a secure key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    email: EmailStr
    password_hash: str


@router.get("/me")
async def get_current_user():
    """Get current authenticated user (placeholder for Auth0 integration)."""
    # TODO: Implement Auth0 token verification
    return {"message": "Auth endpoint - Auth0 integration pending"}


@router.post("/login")
async def login(request: RegisterRequest = Body(...)):
    """Login user, verify password, and return JWT token."""
    user = user_db.get_user(request.email)
    if not user or not pwd_context.verify(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = jwt.encode({
        "sub": user["email"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "email": user["email"], "access_token": access_token}


@router.post("/logout")
async def logout():
    """Logout handler (placeholder)."""
    # TODO: Implement logout
    return {"message": "Logged out"}


@router.post("/register")
async def register(request: RegisterRequest = Body(...)):
    """Register a new user with hashed password and persistent storage."""
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    if user_db.user_exists(request.email):
        raise HTTPException(status_code=409, detail="User already exists")
    password_hash = pwd_context.hash(request.password)
    user_db.add_user(request.email, password_hash)
    return {"message": "User registered", "email": request.email}


@router.get("/profile")
async def get_profile():
    """Get user profile (mock implementation, no authentication)."""
    return {"user": "demo_user", "email": "demo@example.com"}


@router.options("/register")
async def options_register():
    """Handle CORS preflight for /register."""
    from fastapi import Response
    return Response(status_code=200)


@router.options("/{rest_of_path:path}")
async def options_catch_all(rest_of_path: str):
    """Handle CORS preflight for all auth endpoints."""
    from fastapi import Response
    return Response(status_code=200)

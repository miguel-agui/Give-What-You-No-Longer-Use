from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.services.database import get_db, create_user, get_user_by_email, get_user, update_user
from app.auth.auth_handler import (
    get_current_user, 
    create_access_token, 
    verify_password,
    get_password_hash
)
from typing import List

router = APIRouter(tags=["users"])

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get JWT token"""
    user = get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=UserRead)
async def update_user_me(user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update current user information"""
    return update_user(db, current_user.id, user)

@router.post("/change-password")
async def change_password(
    old_password: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password"""
    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    hashed_password = get_password_hash(new_password)
    db_user = get_user(db, current_user.id)
    db_user.hashed_password = hashed_password
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Password updated successfully"}

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

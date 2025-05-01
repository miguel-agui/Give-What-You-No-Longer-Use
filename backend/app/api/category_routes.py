from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.database import get_db, create_category, get_category, get_categories, update_category

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryRead)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    return create_category(db, category)

@router.get("/", response_model=List[CategoryRead])
def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
    db: Session = Depends(get_db)
):
    """Get all categories with optional parent_id filter"""
    return get_categories(db, skip=skip, limit=limit, parent_id=parent_id)

@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    db_category = get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category_by_id(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Update a category"""
    db_category = update_category(db, category_id, category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Soft delete a category by setting is_active to False"""
    db_category = get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Soft delete by setting is_active to False
    db_category = update_category(db, category_id, CategoryUpdate(is_active=False))
    return db_category

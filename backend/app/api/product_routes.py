from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.models.product import ProductCreate, ProductRead, ProductUpdate, ProductImageCreate, ProductImageRead
class ProductFilter(BaseModel):
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    search: Optional[str] = None
    sort_by: Optional[str] = None
    is_sold: Optional[bool] = False

from app.services.database import get_db, create_product, get_product, get_products, update_product, add_product_image
from app.auth.auth_handler import get_current_user
from app.models.user import User
import json

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductRead)
async def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new product listing"""
    return create_product(db, product, current_user.id)

@router.get("/", response_model=List[ProductRead])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    filter: ProductFilter = Depends(),
    db: Session = Depends(get_db)
):
    """Get all active products with optional filters"""
    filters = filter.dict(exclude_unset=True)
    return get_products(db, skip=skip, limit=limit, filters=filters)
@router.patch("/{product_id}", response_model=ProductRead)
async def patch_product_by_id(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Partially update a product"""
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    return update_product(db, product_id, product)

@router.post("/batch", response_model=List[ProductRead])
async def create_products_batch(
    products: List[ProductCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create multiple products in a batch operation"""
    created_products = []
    for product in products:
        created = create_product(db, product, current_user.id)
        created_products.append(created)
    return created_products

@router.get("/user/{user_id}", response_model=List[ProductRead])
async def read_user_products(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    include_sold: bool = False,
    db: Session = Depends(get_db)
):
    """Get all products for a specific user"""
    filters = {
        "user_id": user_id,
        "is_sold": None if include_sold else False
    }
    return get_products(db, skip=skip, limit=limit, filters=filters)

@router.get("/my-products", response_model=List[ProductRead])
async def read_my_products(
    skip: int = 0,
    limit: int = 100,
    include_sold: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all products for the current user"""
    filters = {
        "user_id": current_user.id,
        "is_sold": None if include_sold else False
    }
    return get_products(db, skip=skip, limit=limit, filters=filters)

@router.get("/{product_id}", response_model=ProductRead)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductRead)
async def update_product_by_id(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a product"""
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if the product belongs to the current user
    if db_product.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    
    return update_product(db, product_id, product)

@router.post("/{product_id}/images", response_model=ProductImageRead)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    is_primary: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload an image for a product"""
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if the product belongs to the current user
    if db_product.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")
    
    # Here we would normally upload the image to a storage service like Azure Blob Storage
    # For now, we'll just simulate it and return a placeholder URL
    # In a real implementation, this would be replaced with actual file upload code
    
    # Placeholder for image upload - in production this would be Azure Blob Storage
    image_url = f"https://storage.example.com/products/{product_id}/{file.filename}"
    
    image_create = ProductImageCreate(
        image_url=image_url,
        is_primary=is_primary
    )
    
    return add_product_image(db, product_id, image_create)

@router.delete("/{product_id}", response_model=ProductRead)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete a product by setting is_active to False"""
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if the product belongs to the current user
    if db_product.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")
    
    # Soft delete by setting is_active to False
    return update_product(db, product_id, ProductUpdate(is_active=False))

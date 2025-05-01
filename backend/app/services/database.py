from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker, Session
from app.models.user import User, UserCreate, UserUpdate
from app.models.product import Product, ProductCreate, ProductUpdate, ProductImage, ProductImageCreate
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionStatus
from passlib.context import CryptContext
from typing import List, Optional, Dict, Any
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # For demo; use PostgreSQL for production

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User operations
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
        
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

# Category operations
def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100, parent_id: Optional[int] = None):
    query = db.query(Category).filter(Category.is_active == True)
    if parent_id is not None:
        query = query.filter(Category.parent_id == parent_id)
    return query.offset(skip).limit(limit).all()

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
        
    update_data = category_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
        
    db.commit()
    db.refresh(db_category)
    return db_category

# Product operations
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None):
    query = db.query(Product).filter(Product.is_active == True)
    
    if filters:
        if 'category_id' in filters and filters['category_id']:
            query = query.filter(Product.category_id == filters['category_id'])
        if 'user_id' in filters and filters['user_id']:
            query = query.filter(Product.user_id == filters['user_id'])
        if 'is_sold' in filters:
            query = query.filter(Product.is_sold == filters['is_sold'])
        if 'min_price' in filters and filters['min_price'] is not None:
            query = query.filter(Product.price >= filters['min_price'])
        if 'max_price' in filters and filters['max_price'] is not None:
            query = query.filter(Product.price <= filters['max_price'])
        if 'search' in filters and filters['search']:
            search = f"%{filters['search']}%"
            query = query.filter(Product.title.like(search) | Product.description.like(search))
        if 'sort_by' in filters and filters['sort_by']:
            if filters['sort_by'] == 'price_asc':
                query = query.order_by(asc(Product.price))
            elif filters['sort_by'] == 'price_desc':
                query = query.order_by(desc(Product.price))
            elif filters['sort_by'] == 'date_desc':
                query = query.order_by(desc(Product.created_at))
            else:  # Default to newest first
                query = query.order_by(desc(Product.created_at))
        else:
            query = query.order_by(desc(Product.created_at))
    else:
        query = query.order_by(desc(Product.created_at))
        
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate, user_id: int):
    db_product = Product(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
        
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db_product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_product)
    return db_product

def add_product_image(db: Session, product_id: int, image: ProductImageCreate):
    db_image = ProductImage(**image.dict(), product_id=product_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

# Transaction operations
def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_user_transactions(db: Session, user_id: int, as_buyer: bool = True, skip: int = 0, limit: int = 100):
    if as_buyer:
        return db.query(Transaction).filter(Transaction.buyer_id == user_id).order_by(desc(Transaction.created_at)).offset(skip).limit(limit).all()
    else:
        return db.query(Transaction).filter(Transaction.seller_id == user_id).order_by(desc(Transaction.created_at)).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: TransactionCreate, payment_id: str):
    db_transaction = Transaction(
        **transaction.dict(),
        payment_id=payment_id,
        status=TransactionStatus.PENDING
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction_status(db: Session, transaction_id: int, status: TransactionStatus):
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None
        
    db_transaction.status = status
    db_transaction.updated_at = datetime.utcnow()
    
    # If transaction is completed, mark product as sold
    if status == TransactionStatus.COMPLETED:
        product = get_product(db, db_transaction.product_id)
        if product:
            product.is_sold = True
            product.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

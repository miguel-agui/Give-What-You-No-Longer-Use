from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import user_routes, category_routes, product_routes, transaction_routes, moderation_routes, payment_routes
from app.models import user, product, category, transaction
from app.services.database import engine
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.auth.auth_handler import get_current_active_admin

# Create database tables
user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)
category.Base.metadata.create_all(bind=engine)
transaction.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Circular Economy Platform API",
    description="API for a circular economy marketplace platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router, prefix="/api")
app.include_router(category_routes.router, prefix="/api")
app.include_router(product_routes.router, prefix="/api")
app.include_router(transaction_routes.router, prefix="/api")
app.include_router(moderation_routes.router, prefix="/api")
app.include_router(payment_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Circular Economy Platform API!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/admin", dependencies=[Depends(get_current_active_admin)])
def admin_only():
    return {"message": "Welcome, admin!"}

# Add a startup event to create initial admin user if none exists
@app.on_event("startup")
async def startup_db_client():
    db = next(get_db())
    try:
        # Check if admin user exists
        admin = db.query(user.User).filter(user.User.is_admin == True).first()
        if not admin:
            # Create admin user
            from app.services.database import create_user
            from app.models.user import UserCreate
            
            admin_user = UserCreate(
                email="admin@example.com",
                password="admin123",  # This should be changed immediately in production
                full_name="System Admin"
            )
            admin = create_user(db, admin_user)
            admin.is_admin = True
            db.commit()
            print("Created default admin user")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

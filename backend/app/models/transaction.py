from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import enum


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)  # ID from payment processor
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product")
    seller = relationship("User", foreign_keys=[seller_id])
    buyer = relationship("User", foreign_keys=[buyer_id])

# Pydantic models for API
class TransactionBase(BaseModel):
    product_id: int
    seller_id: int
    buyer_id: int
    amount: float
    payment_method: str

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus] = None
    payment_id: Optional[str] = None

class TransactionRead(TransactionBase):
    id: int
    payment_id: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

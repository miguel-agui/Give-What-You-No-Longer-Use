from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.transaction import TransactionCreate, TransactionRead, TransactionUpdate, TransactionStatus
from app.models.product import Product
from app.services.database import (
    get_db, create_transaction, get_transaction, get_user_transactions, 
    update_transaction_status, get_product, get_user
)
from app.auth.auth_handler import get_current_user
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionRead)
async def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new transaction
    
    This endpoint would normally integrate with a payment processor like Stripe
    For now, we'll simulate the payment process
    """
    # Verify the buyer is the current user
    if transaction.buyer_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only create transactions for yourself")
    
    # Verify the product exists and is available
    product = get_product(db, transaction.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.is_sold:
        raise HTTPException(status_code=400, detail="Product is already sold")
    
    if not product.is_active:
        raise HTTPException(status_code=400, detail="Product is not available")
    
    # Verify the seller exists
    seller = get_user(db, transaction.seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    # In a real implementation, we would call the payment processor here
    # For now, we'll simulate a payment ID
    payment_id = f"sim_payment_{product.id}_{current_user.id}"
    
    return create_transaction(db, transaction, payment_id)

@router.get("/", response_model=List[TransactionRead])
async def read_transactions(
    as_buyer: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all transactions for the current user"""
    return get_user_transactions(db, current_user.id, as_buyer, skip, limit)

@router.get("/{transaction_id}", response_model=TransactionRead)
async def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific transaction by ID"""
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Check if the user is authorized to view this transaction
    if (transaction.buyer_id != current_user.id and 
        transaction.seller_id != current_user.id and 
        not current_user.is_admin):
        raise HTTPException(status_code=403, detail="Not authorized to view this transaction")
    
    return transaction

@router.put("/{transaction_id}/status", response_model=TransactionRead)
async def update_transaction_status_by_id(
    transaction_id: int,
    status: TransactionStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a transaction status"""
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Only admins can update transaction status
    # In a real app, this would also be triggered by payment webhooks
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update transaction status")
    
    return update_transaction_status(db, transaction_id, status)

@router.post("/{transaction_id}/complete", response_model=TransactionRead)
async def complete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Complete a transaction
    
    This endpoint would normally be called by a webhook from the payment processor
    For demo purposes, we'll allow the seller to manually complete it
    """
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Check if the user is the seller or an admin
    if transaction.seller_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only the seller can complete this transaction")
    
    # Check if the transaction is in a pending state
    if transaction.status != TransactionStatus.PENDING:
        raise HTTPException(
            status_code=400, 
            detail=f"Transaction cannot be completed. Current status: {transaction.status}"
        )
    
    return update_transaction_status(db, transaction_id, TransactionStatus.COMPLETED)

@router.post("/{transaction_id}/cancel", response_model=TransactionRead)
async def cancel_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel a transaction
    
    This can be done by either the buyer or seller
    """
    transaction = get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Check if the user is the buyer, seller, or an admin
    if (transaction.buyer_id != current_user.id and 
        transaction.seller_id != current_user.id and 
        not current_user.is_admin):
        raise HTTPException(status_code=403, detail="Not authorized to cancel this transaction")
    
    # Check if the transaction is in a state that can be cancelled
    if transaction.status not in [TransactionStatus.PENDING]:
        raise HTTPException(
            status_code=400, 
            detail=f"Transaction cannot be cancelled. Current status: {transaction.status}"
        )
    
    return update_transaction_status(db, transaction_id, TransactionStatus.CANCELLED)

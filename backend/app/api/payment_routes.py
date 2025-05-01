from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.services.database import get_db, get_product, get_user, create_transaction, update_transaction_status
from app.auth.auth_handler import get_current_user
from app.models.user import User
from app.models.transaction import TransactionCreate, TransactionStatus
from app.services.payment import create_payment_intent, retrieve_payment_intent, create_refund, verify_webhook_signature, handle_webhook_event
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create-intent")
async def create_payment(
    product_id: int = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a payment intent for purchasing a product
    
    Returns the payment intent details including client secret for frontend integration
    """
    # Get the product
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.is_sold:
        raise HTTPException(status_code=400, detail="Product is already sold")
    
    if not product.is_active:
        raise HTTPException(status_code=400, detail="Product is not available")
    
    # Get the seller
    seller = get_user(db, product.user_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    # Prevent buying your own product
    if seller.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot buy your own product")
    
    # Create metadata for the payment
    metadata = {
        "product_id": str(product.id),
        "product_title": product.title,
        "seller_id": str(seller.id),
        "buyer_id": str(current_user.id)
    }
    
    # Create payment intent
    payment_intent = create_payment_intent(
        amount=product.price,
        currency="usd",  # This should be configurable
        metadata=metadata
    )
    
    if "error" in payment_intent:
        raise HTTPException(status_code=500, detail=payment_intent["error"])
    
    # Create a transaction record
    transaction = TransactionCreate(
        product_id=product.id,
        seller_id=seller.id,
        buyer_id=current_user.id,
        amount=product.price,
        payment_method="card"  # This should be dynamic based on the payment method
    )
    
    db_transaction = create_transaction(db, transaction, payment_intent["id"])
    
    return {
        "payment_intent": payment_intent,
        "transaction_id": db_transaction.id,
        "product": {
            "id": product.id,
            "title": product.title,
            "price": product.price
        }
    }

@router.get("/intent/{payment_intent_id}")
async def get_payment_status(
    payment_intent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check the status of a payment intent
    
    Returns the current status and details of the payment
    """
    payment_intent = retrieve_payment_intent(payment_intent_id)
    
    if "error" in payment_intent:
        raise HTTPException(status_code=500, detail=payment_intent["error"])
    
    return payment_intent

@router.post("/refund")
async def refund_payment(
    payment_intent_id: str = Body(...),
    amount: Optional[float] = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a refund for a payment
    
    Only available to admins or the seller of the product
    """
    # Only admins can process refunds for now
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only administrators can process refunds")
    
    refund = create_refund(payment_intent_id, amount)
    
    if "error" in refund:
        raise HTTPException(status_code=500, detail=refund["error"])
    
    return refund

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhook events
    
    This endpoint receives events from Stripe about payment status changes
    """
    # Get the signature from the header
    signature = request.headers.get("stripe-signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing Stripe signature")
    
    # Get the raw request body
    payload = await request.body()
    
    # Verify the signature
    if not verify_webhook_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    
    # Handle the event
    event_data = handle_webhook_event(payload, signature)
    
    if "error" in event_data:
        logger.error(f"Error handling webhook: {event_data['error']}")
        return {"status": "error", "message": event_data["error"]}
    
    # Process the event
    if event_data["event_type"] == "payment_intent.succeeded":
        # Update transaction status in the database
        db = next(get_db())
        try:
            # Find transactions with this payment ID
            payment_intent_id = event_data["payment_intent_id"]
            
            # Update transaction status to completed
            # In a real implementation, you would look up the transaction by payment_intent_id
            # For now, we'll assume there's a function to find and update it
            
            # This is a placeholder - in production you would implement proper transaction lookup
            # transaction = get_transaction_by_payment_id(db, payment_intent_id)
            # if transaction:
            #     update_transaction_status(db, transaction.id, TransactionStatus.COMPLETED)
            
            logger.info(f"Payment succeeded: {payment_intent_id}")
        finally:
            db.close()
    
    return {"status": "success", "event_processed": event_data["event_type"]}

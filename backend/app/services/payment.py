import stripe
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stripe configuration
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
AZURE_KEYVAULT_URL = os.getenv("AZURE_KEYVAULT_URL")

# Initialize Stripe
def initialize_stripe():
    """Initialize the Stripe client"""
    global STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET
    
    try:
        # Try to get credentials from Key Vault if URL is provided
        if AZURE_KEYVAULT_URL:
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=AZURE_KEYVAULT_URL, credential=credential)
            STRIPE_API_KEY = secret_client.get_secret("StripeApiKey").value
            STRIPE_WEBHOOK_SECRET = secret_client.get_secret("StripeWebhookSecret").value
        
        if STRIPE_API_KEY:
            stripe.api_key = STRIPE_API_KEY
            logger.info("Stripe client initialized successfully")
        else:
            logger.warning("Stripe API key not found")
    except Exception as e:
        logger.error(f"Failed to initialize Stripe client: {str(e)}")

# Initialize on module import
initialize_stripe()

# Payment functions
def create_payment_intent(amount: float, currency: str = "usd", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a payment intent with Stripe
    
    Args:
        amount: Amount in smallest currency unit (e.g., cents for USD)
        currency: Three-letter ISO currency code
        metadata: Additional metadata for the payment
    
    Returns:
        Dict containing payment intent details
    """
    if not stripe.api_key:
        initialize_stripe()
        if not stripe.api_key:
            logger.error("Stripe API key not available")
            return {"error": "Payment service not available"}
    
    try:
        # Convert float amount to integer cents
        amount_cents = int(amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={"enabled": True}
        )
        
        return {
            "id": intent.id,
            "client_secret": intent.client_secret,
            "amount": amount,
            "currency": currency,
            "status": intent.status
        }
    except Exception as e:
        logger.error(f"Error creating payment intent: {str(e)}")
        return {"error": str(e)}

def retrieve_payment_intent(payment_intent_id: str) -> Dict[str, Any]:
    """
    Retrieve a payment intent from Stripe
    
    Args:
        payment_intent_id: The ID of the payment intent to retrieve
    
    Returns:
        Dict containing payment intent details
    """
    if not stripe.api_key:
        initialize_stripe()
        if not stripe.api_key:
            logger.error("Stripe API key not available")
            return {"error": "Payment service not available"}
    
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        return {
            "id": intent.id,
            "amount": intent.amount / 100,  # Convert cents to dollars
            "currency": intent.currency,
            "status": intent.status,
            "metadata": intent.metadata
        }
    except Exception as e:
        logger.error(f"Error retrieving payment intent: {str(e)}")
        return {"error": str(e)}

def create_refund(payment_intent_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
    """
    Create a refund for a payment intent
    
    Args:
        payment_intent_id: The ID of the payment intent to refund
        amount: Amount to refund (if None, refund the entire amount)
    
    Returns:
        Dict containing refund details
    """
    if not stripe.api_key:
        initialize_stripe()
        if not stripe.api_key:
            logger.error("Stripe API key not available")
            return {"error": "Payment service not available"}
    
    try:
        refund_params = {"payment_intent": payment_intent_id}
        
        if amount is not None:
            # Convert float amount to integer cents
            amount_cents = int(amount * 100)
            refund_params["amount"] = amount_cents
        
        refund = stripe.Refund.create(**refund_params)
        
        return {
            "id": refund.id,
            "amount": refund.amount / 100,  # Convert cents to dollars
            "currency": refund.currency,
            "status": refund.status,
            "payment_intent_id": payment_intent_id
        }
    except Exception as e:
        logger.error(f"Error creating refund: {str(e)}")
        return {"error": str(e)}

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify the signature of a Stripe webhook
    
    Args:
        payload: The raw request body from Stripe
        signature: The signature header from Stripe
    
    Returns:
        Boolean indicating whether the signature is valid
    """
    if not STRIPE_WEBHOOK_SECRET:
        logger.error("Stripe webhook secret not available")
        return False
    
    try:
        stripe.Webhook.construct_event(
            payload, signature, STRIPE_WEBHOOK_SECRET
        )
        return True
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {str(e)}")
        return False

def handle_webhook_event(payload: bytes, signature: str) -> Dict[str, Any]:
    """
    Handle a Stripe webhook event
    
    Args:
        payload: The raw request body from Stripe
        signature: The signature header from Stripe
    
    Returns:
        Dict containing the processed event
    """
    if not STRIPE_WEBHOOK_SECRET:
        logger.error("Stripe webhook secret not available")
        return {"error": "Webhook secret not configured"}
    
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, STRIPE_WEBHOOK_SECRET
        )
        
        event_type = event['type']
        data = event['data']['object']
        
        # Handle different event types
        if event_type == 'payment_intent.succeeded':
            # Payment was successful
            return {
                "status": "success",
                "event_type": event_type,
                "payment_intent_id": data['id'],
                "amount": data['amount'] / 100,
                "currency": data['currency'],
                "metadata": data['metadata']
            }
        elif event_type == 'payment_intent.payment_failed':
            # Payment failed
            return {
                "status": "failed",
                "event_type": event_type,
                "payment_intent_id": data['id'],
                "error": data.get('last_payment_error', {}).get('message', 'Unknown error')
            }
        else:
            # Other event types
            return {
                "status": "received",
                "event_type": event_type,
                "data": data
            }
    except Exception as e:
        logger.error(f"Error handling webhook event: {str(e)}")
        return {"error": str(e)}

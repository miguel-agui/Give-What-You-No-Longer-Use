from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient, ImageAnalysisOptions
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure configuration
AZURE_TEXT_ANALYTICS_ENDPOINT = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
AZURE_TEXT_ANALYTICS_KEY = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
AZURE_KEYVAULT_URL = os.getenv("AZURE_KEYVAULT_URL")

# Initialize clients
text_analytics_client = None
vision_client = None

def initialize_text_analytics():
    """Initialize the Text Analytics client"""
    global text_analytics_client
    
    try:
        # Try to get credentials from Key Vault if URL is provided
        if AZURE_KEYVAULT_URL:
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=AZURE_KEYVAULT_URL, credential=credential)
            text_key = secret_client.get_secret("TextAnalyticsKey").value
            text_endpoint = secret_client.get_secret("TextAnalyticsEndpoint").value
        else:
            # Fall back to environment variables
            text_key = AZURE_TEXT_ANALYTICS_KEY
            text_endpoint = AZURE_TEXT_ANALYTICS_ENDPOINT
        
        if text_key and text_endpoint:
            text_analytics_client = TextAnalyticsClient(
                endpoint=text_endpoint, 
                credential=AzureKeyCredential(text_key)
            )
            logger.info("Text Analytics client initialized successfully")
        else:
            logger.warning("Text Analytics credentials not found")
    except Exception as e:
        logger.error(f"Failed to initialize Text Analytics client: {str(e)}")

def initialize_vision():
    """Initialize the Vision client"""
    global vision_client
    
    try:
        # Try to get credentials from Key Vault if URL is provided
        if AZURE_KEYVAULT_URL:
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=AZURE_KEYVAULT_URL, credential=credential)
            vision_key = secret_client.get_secret("VisionKey").value
            vision_endpoint = secret_client.get_secret("VisionEndpoint").value
        else:
            # Fall back to environment variables
            vision_key = AZURE_VISION_KEY
            vision_endpoint = AZURE_VISION_ENDPOINT
        
        if vision_key and vision_endpoint:
            vision_client = ImageAnalysisClient(
                endpoint=vision_endpoint,
                credential=AzureKeyCredential(vision_key)
            )
            logger.info("Vision client initialized successfully")
        else:
            logger.warning("Vision credentials not found")
    except Exception as e:
        logger.error(f"Failed to initialize Vision client: {str(e)}")

def initialize_clients():
    """Initialize all Azure AI clients"""
    initialize_text_analytics()
    initialize_vision()

# Content moderation functions
def moderate_text(text: str, language: str = "en") -> Dict[str, Any]:
    """
    Moderate text content using Azure Text Analytics
    
    Returns a dict with:
    - is_appropriate: bool
    - categories: List of detected categories
    - confidence_scores: Dict of category confidence scores
    - language: Detected language
    """
    if not text_analytics_client:
        initialize_text_analytics()
        if not text_analytics_client:
            logger.error("Text Analytics client not available")
            return {"is_appropriate": True, "error": "Text Analytics service not available"}
    
    try:
        # Detect language if not provided
        if not language:
            language_response = text_analytics_client.detect_language([text])
            language = language_response[0].primary_language.iso6391_name
        
        # Analyze sentiment
        sentiment_response = text_analytics_client.analyze_sentiment([text], language=language)
        sentiment = sentiment_response[0]
        
        # Detect key phrases
        key_phrases_response = text_analytics_client.extract_key_phrases([text], language=language)
        key_phrases = key_phrases_response[0].key_phrases if not key_phrases_response[0].is_error else []
        
        # Recognize entities
        entities_response = text_analytics_client.recognize_entities([text], language=language)
        entities = entities_response[0].entities if not entities_response[0].is_error else []
        
        # Check for inappropriate content
        # This is a simplified approach - in production, you would use a more sophisticated algorithm
        # or a dedicated content moderation service
        inappropriate_keywords = ["scam", "illegal", "fraud", "counterfeit", "fake", "stolen"]
        contains_inappropriate = any(keyword in text.lower() for keyword in inappropriate_keywords)
        
        # Check sentiment - very negative content might need review
        is_very_negative = sentiment.confidence_scores.negative > 0.8
        
        result = {
            "is_appropriate": not (contains_inappropriate or is_very_negative),
            "sentiment": {
                "positive": sentiment.confidence_scores.positive,
                "neutral": sentiment.confidence_scores.neutral,
                "negative": sentiment.confidence_scores.negative
            },
            "key_phrases": key_phrases,
            "entities": [{"text": e.text, "category": e.category} for e in entities],
            "language": language
        }
        
        return result
    
    except Exception as e:
        logger.error(f"Error in text moderation: {str(e)}")
        return {"is_appropriate": True, "error": str(e)}

def analyze_image(image_url: str) -> Dict[str, Any]:
    """
    Analyze an image using Azure Computer Vision
    
    Returns a dict with:
    - is_appropriate: bool
    - tags: List of detected tags
    - objects: List of detected objects
    - description: Auto-generated image description
    - adult_content: Information about adult content detection
    """
    if not vision_client:
        initialize_vision()
        if not vision_client:
            logger.error("Vision client not available")
            return {"is_appropriate": True, "error": "Vision service not available"}
    
    try:
        # Set analysis options
        analysis_options = ImageAnalysisOptions()
        analysis_options.features = (
            "Tags,Objects,Caption,DenseCaptions,SmartCrops,People"
        )
        analysis_options.language = "en"
        
        # Analyze the image
        result = vision_client.analyze(image_url, analysis_options)
        
        # Extract relevant information
        tags = [tag.name for tag in result.tags] if result.tags else []
        objects = [obj.name for obj in result.objects] if result.objects else []
        caption = result.caption.text if result.caption else ""
        
        # Check for inappropriate content
        # This is a simplified approach - in production, you would use a more sophisticated algorithm
        inappropriate_tags = ["weapon", "drugs", "violence", "adult"]
        contains_inappropriate = any(tag.lower() in inappropriate_tags for tag in tags)
        
        return {
            "is_appropriate": not contains_inappropriate,
            "tags": tags,
            "objects": objects,
            "caption": caption,
            "people_count": len(result.people) if result.people else 0
        }
    
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        return {"is_appropriate": True, "error": str(e)}

# Initialize clients on module import
initialize_clients()

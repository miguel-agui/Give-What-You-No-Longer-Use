from fastapi import APIRouter, Depends, HTTPException, Body, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.services.database import get_db
from app.auth.auth_handler import get_current_user
from app.models.user import User
from app.services.azure_ai import moderate_text, analyze_image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/moderation", tags=["moderation"])

@router.post("/text")
async def check_text_content(
    text: str = Body(..., description="Text content to moderate"),
    language: Optional[str] = Body(None, description="ISO language code (e.g., 'en')"),
    current_user: User = Depends(get_current_user)
):
    """
    Moderate text content using Azure AI
    
    Returns analysis of the text including appropriateness, sentiment, and entities
    """
    try:
        result = moderate_text(text, language)
        return result
    except Exception as e:
        logger.error(f"Error in text moderation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in text moderation: {str(e)}")

@router.post("/image")
async def check_image_content(
    image_url: str = Body(..., description="URL of the image to analyze"),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze image content using Azure AI Vision
    
    Returns analysis of the image including appropriateness, tags, and objects
    """
    try:
        result = analyze_image(image_url)
        return result
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in image analysis: {str(e)}")

@router.post("/product")
async def moderate_product_listing(
    title: str = Body(...),
    description: str = Body(...),
    image_urls: list[str] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Moderate a complete product listing including text and images
    
    Returns a comprehensive moderation result for the entire listing
    """
    try:
        # Moderate text content
        title_result = moderate_text(title)
        description_result = moderate_text(description)
        
        # Analyze images
        image_results = []
        for url in image_urls:
            image_result = analyze_image(url)
            image_results.append(image_result)
        
        # Determine overall appropriateness
        text_appropriate = title_result.get("is_appropriate", True) and description_result.get("is_appropriate", True)
        images_appropriate = all(result.get("is_appropriate", True) for result in image_results)
        
        return {
            "is_appropriate": text_appropriate and images_appropriate,
            "text_moderation": {
                "title": title_result,
                "description": description_result
            },
            "image_moderation": image_results
        }
    except Exception as e:
        logger.error(f"Error in product moderation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in product moderation: {str(e)}")

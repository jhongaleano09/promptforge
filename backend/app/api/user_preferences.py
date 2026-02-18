"""
User preferences API endpoints.

Handles user profile and preferences management.
Single-user application: only one preferences row exists.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.user_service import user_preferences_service
from app.api.schemas import (
    UserPreferencesResponse,
    UserPreferencesUpdate,
    LanguagePreferenceResponse,
    LanguagePreferenceUpdate
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(db: Session = Depends(get_db)):
    """
    Get all user preferences.

    Returns:
        UserPreferencesResponse with all user preferences
    """
    try:
        prefs = user_preferences_service.get_or_create_preferences(db)

        return UserPreferencesResponse(
            language=prefs.language,
            name=prefs.name,
            country=prefs.country,
            default_provider=prefs.default_provider,
            default_model=prefs.default_model,
            auto_save_preferences=prefs.auto_save_preferences,
            theme=prefs.theme
        )
    except Exception as e:
        logger.error(f"Error getting user preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user preferences")


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    preferences: UserPreferencesUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user preferences.

    Only provided fields will be updated.

    Args:
        preferences: UserPreferencesUpdate object with optional fields

    Returns:
        Updated UserPreferencesResponse

    Raises:
        HTTPException 400: If language or provider/theme is invalid
    """
    try:
        # Update preferences (only provided fields)
        prefs = user_preferences_service.update_preferences(
            db,
            language=preferences.language,
            name=preferences.name,
            country=preferences.country,
            default_provider=preferences.default_provider,
            default_model=preferences.default_model,
            auto_save_preferences=preferences.auto_save_preferences,
            theme=preferences.theme
        )

        return UserPreferencesResponse(
            language=prefs.language,
            name=prefs.name,
            country=prefs.country,
            default_provider=prefs.default_provider,
            default_model=prefs.default_model,
            auto_save_preferences=prefs.auto_save_preferences,
            theme=prefs.theme
        )
    except ValueError as e:
        # Invalid language or provider or theme
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user preferences")


@router.get("/preferences/language", response_model=LanguagePreferenceResponse)
async def get_language_preference(db: Session = Depends(get_db)):
    """
    Get the current language preference.
    
    Returns:
        LanguagePreferenceResponse with current language and supported languages
    """
    try:
        language = user_preferences_service.get_language(db)
        
        return LanguagePreferenceResponse(
            language=language,
            supported_languages=["spanish", "english"]
        )
    except Exception as e:
        logger.error(f"Error getting language preference: {e}")
        raise HTTPException(status_code=500, detail="Failed to get language preference")


@router.put("/preferences/language", response_model=LanguagePreferenceResponse)
async def update_language_preference(
    language_update: LanguagePreferenceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the language preference.
    
    Args:
        language_update: LanguagePreferenceUpdate object with language field
        
    Returns:
        Updated LanguagePreferenceResponse
        
    Raises:
        HTTPException 400: If language is invalid
    """
    try:
        language = user_preferences_service.set_language(db, language_update.language)
        
        return LanguagePreferenceResponse(
            language=language,
            supported_languages=["spanish", "english"]
        )
    except ValueError as e:
        # Invalid language
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating language preference: {e}")
        raise HTTPException(status_code=500, detail="Failed to update language preference")

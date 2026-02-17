"""
User preferences service.

Handles business logic for user profile and preferences.
This is a single-user application, so there should only be one row in the database.
"""

from sqlalchemy.orm import Session
from app.db.models import UserPreferences
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class UserPreferencesService:
    """
    Service for managing user preferences.
    
    Single-user application: only one preferences row should exist.
    """
    
    @staticmethod
    def get_preferences(db: Session) -> Optional[UserPreferences]:
        """
        Get the user preferences (single row).
        
        Returns:
            UserPreferences object or None if not found
        """
        return db.query(UserPreferences).first()
    
    @staticmethod
    def get_or_create_preferences(db: Session) -> UserPreferences:
        """
        Get existing preferences or create default ones if they don't exist.
        
        Returns:
            UserPreferences object (always returns a valid object)
        """
        prefs = UserPreferencesService.get_preferences(db)
        
        if not prefs:
            # Create default preferences
            prefs = UserPreferences(
                language="spanish",
                name=None,
                country=None
            )
            db.add(prefs)
            db.commit()
            db.refresh(prefs)
            logger.info("Created default user preferences")
        
        return prefs
    
    @staticmethod
    def update_preferences(
        db: Session,
        language: Optional[str] = None,
        name: Optional[str] = None,
        country: Optional[str] = None
    ) -> UserPreferences:
        """
        Update user preferences.
        
        Args:
            db: Database session
            language: New language preference (optional)
            name: New user name (optional)
            country: New country (optional)
            
        Returns:
            Updated UserPreferences object
            
        Raises:
            ValueError: If language is invalid
        """
        # Validate language if provided
        if language is not None:
            language_lower = language.lower().strip()
            if language_lower not in ["spanish", "english"]:
                raise ValueError(
                    f"Invalid language: {language}. Must be 'spanish' or 'english'"
                )
            language = language_lower
        
        # Get or create preferences
        prefs = UserPreferencesService.get_or_create_preferences(db)
        
        # Update fields if provided
        if language is not None:
            prefs.language = language
        if name is not None:
            prefs.name = name
        if country is not None:
            prefs.country = country
        
        db.commit()
        db.refresh(prefs)
        
        logger.info(f"Updated user preferences: language={prefs.language}, name={prefs.name}, country={prefs.country}")
        
        return prefs
    
    @staticmethod
    def get_language(db: Session) -> str:
        """
        Get the current language preference.
        
        Returns:
            Language code ('spanish' or 'english')
        """
        prefs = UserPreferencesService.get_or_create_preferences(db)
        return prefs.language
    
    @staticmethod
    def set_language(db: Session, language: str) -> str:
        """
        Set the language preference.
        
        Args:
            db: Database session
            language: Language code ('spanish' or 'english')
            
        Returns:
            The updated language code
            
        Raises:
            ValueError: If language is invalid
        """
        prefs = UserPreferencesService.update_preferences(db, language=language)
        return prefs.language


# Singleton instance
user_preferences_service = UserPreferencesService()

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
                country=None,
                default_provider="openai",
                default_model="gpt-4-turbo",
                auto_save_preferences=True,
                theme="light"
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
        country: Optional[str] = None,
        default_provider: Optional[str] = None,
        default_model: Optional[str] = None,
        auto_save_preferences: Optional[bool] = None,
        theme: Optional[str] = None
    ) -> UserPreferences:
        """
        Update user preferences.

        Args:
            db: Database session
            language: New language preference (optional)
            name: New user name (optional)
            country: New country (optional)
            default_provider: Default LLM provider (optional)
            default_model: Default model preference (optional)
            auto_save_preferences: Auto-save preference (optional)
            theme: UI theme (optional)

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

        # Validate provider if provided
        if default_provider is not None:
            provider_lower = default_provider.lower().strip()
            if provider_lower not in ["openai", "anthropic", "ollama"]:
                raise ValueError(
                    f"Invalid provider: {default_provider}. Must be 'openai', 'anthropic', or 'ollama'"
                )
            default_provider = provider_lower

        # Validate theme if provided
        if theme is not None:
            theme_lower = theme.lower().strip()
            if theme_lower not in ["light", "dark"]:
                raise ValueError(
                    f"Invalid theme: {theme}. Must be 'light' or 'dark'"
                )
            theme = theme_lower

        # Get or create preferences
        prefs = UserPreferencesService.get_or_create_preferences(db)

        # Update fields if provided
        if language is not None:
            prefs.language = language
        if name is not None:
            prefs.name = name
        if country is not None:
            prefs.country = country
        if default_provider is not None:
            prefs.default_provider = default_provider
        if default_model is not None:
            prefs.default_model = default_model
        if auto_save_preferences is not None:
            prefs.auto_save_preferences = auto_save_preferences
        if theme is not None:
            prefs.theme = theme

        db.commit()
        db.refresh(prefs)

        logger.info(f"Updated user preferences: language={prefs.language}, name={prefs.name}, country={prefs.country}, "
                   f"provider={prefs.default_provider}, model={prefs.default_model}, theme={prefs.theme}")

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

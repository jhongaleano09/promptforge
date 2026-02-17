"""
Helper functions for agent nodes.

This module provides utility functions that nodes can use to access
templates, validate state, and perform common operations.
"""

from typing import Dict, Any
from app.prompts.i18n_templates import get_templates, is_valid_language


def get_node_templates(state: Dict[str, Any]) -> Dict[str, str]:
    """
    Obtains templates according to the language in the state.
    Centralizes the logic for all nodes.
    
    This function:
    1. Extracts the 'language' field from the state
    2. Falls back to 'spanish' if not present or invalid
    3. Returns the appropriate template dictionary
    
    Args:
        state: The PromptState dictionary containing workflow state
        
    Returns:
        Dictionary with template keys: 'clarifier', 'generator', 'evaluator', 'judge', 'refiner'
        
    Example:
        >>> from app.agents.state import PromptState
        >>> state = PromptState(language="english", user_input="Help me")
        >>> templates = get_node_templates(state)
        >>> clarifier_prompt = templates["clarifier"].format(...)
    """
    # Get language from state, default to 'spanish'
    language = state.get("language", "spanish")
    
    # Validate language, fallback to spanish if invalid
    if not is_valid_language(language):
        language = "spanish"
    
    # Return templates for the specified language
    return get_templates(language)


def get_interaction_language_name(state: Dict[str, Any]) -> str:
    """
    Returns the display name of the interaction language.
    
    Useful for inserting into prompts that reference the language name.
    
    Args:
        state: The PromptState dictionary
        
    Returns:
        Display name: "Spanish" or "English"
        
    Example:
        >>> state = {"language": "spanish"}
        >>> get_interaction_language_name(state)
        'Spanish'
    """
    language = state.get("language", "spanish")
    
    # Return capitalized name for use in prompts
    if language.lower() == "english":
        return "English"
    else:
        return "Spanish"

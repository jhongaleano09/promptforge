"""
Prompt Types Configuration Module

Defines all supported prompt types and their configurations.
This module provides the foundation for the modular prompt system.
"""

from enum import Enum
from typing import Dict, Any, List


class PromptType(Enum):
    """Enumeration of supported prompt types."""
    BASIC = "basic"            # ✅ Enabled (already functional)
    SYSTEM = "system"          # ⏳ Phase 8.6 will enable this
    IMAGE = "image"            # ⏳ Phase 8.7 will enable this
    ADDITIONAL = "additional"  # ⏳ Phase 8.8 will enable this


# Configuration for each prompt type
PROMPT_TYPE_CONFIGS: Dict[str, Dict[str, Any]] = {
    PromptType.BASIC.value: {
        "name": "Basic Prompt",
        "description": "Standard prompt for general prompt engineering tasks",
        "requires_test_input": False,
        "workflow_graph": "basic_workflow",
        "enabled": True,  # Available for use
        "icon": "📝",
        "color": "blue",
        "category": "general",
        "recommended_models": ["gpt-4o", "claude-3-5-sonnet-20241022", "glm-4-plus"],
        "tags": ["general", "beginner-friendly", "versatile"]
    },
    PromptType.SYSTEM.value: {
        "name": "System Prompt",
        "description": "System prompt to configure model behavior and role",
        "requires_test_input": True,  # Requires user input for testing
        "workflow_graph": "system_prompt_workflow",
        "enabled": True,  # ✅ Enabled in Sprint 4
        "icon": "⚙️",
        "color": "purple",
        "category": "configuration",
        "recommended_models": ["gpt-4o", "claude-3-5-sonnet-20241022"],
        "tags": ["advanced", "configuration", "role-definition"]
    },
    PromptType.IMAGE.value: {
        "name": "Image Prompt",
        "description": "Specialized prompt for image generation (DALL-E, Midjourney, Stable Diffusion)",
        "requires_test_input": False,
        "workflow_graph": "image_prompt_workflow",
        "enabled": True,  # ✅ Enabled in Sprint 4
        "icon": "🖼️",
        "color": "green",
        "category": "creative",
        "recommended_models": ["gpt-4o", "claude-3-5-sonnet-20241022"],
        "tags": ["creative", "visual", "image-generation"]
    },
    PromptType.ADDITIONAL.value: {
        "name": "Additional Prompt",
        "description": "Complementary prompt for specific tasks with variable placeholders",
        "requires_test_input": False,
        "workflow_graph": "additional_prompt_workflow",
        "enabled": True,  # ✅ Enabled in Sprint 4
        "icon": "➕",
        "color": "orange",
        "category": "extension",
        "recommended_models": ["gpt-4o", "claude-3-5-sonnet-20241022", "glm-4-plus"],
        "tags": ["templates", "variables", "reusable"]
    }
}


# --- Helper Functions ---

def get_prompt_type_config(prompt_type: str) -> Dict[str, Any]:
    """
    Returns the configuration for a specific prompt type.
    
    Args:
        prompt_type: String of the type (e.g., 'basic', 'system', 'image', 'additional')
    
    Returns:
        Dict with type configuration.
    
    Raises:
        ValueError: If the prompt type doesn't exist.
    """
    config = PROMPT_TYPE_CONFIGS.get(prompt_type)
    if not config:
        raise ValueError(
            f"Prompt type '{prompt_type}' not supported. "
            f"Available types: {list(PROMPT_TYPE_CONFIGS.keys())}"
        )
    return config


def get_enabled_prompt_types() -> List[str]:
    """
    Returns list of enabled prompt types (enabled = True).
    
    Returns:
        List of strings with IDs of enabled types.
    """
    return [
        ptype for ptype, config in PROMPT_TYPE_CONFIGS.items()
        if config.get("enabled", False)
    ]


def get_all_prompt_types() -> List[Dict[str, Any]]:
    """
    Returns list of all prompt types with their configurations.
    
    Returns:
        List of dicts with complete information for each type.
    """
    return [
        {
            "id": ptype,
            **config
        }
        for ptype, config in PROMPT_TYPE_CONFIGS.items()
    ]


def is_prompt_type_enabled(prompt_type: str) -> bool:
    """
    Verifies if a prompt type is enabled.
    
    Args:
        prompt_type: String of the type to verify
    
    Returns:
        True if enabled, False otherwise.
    """
    config = PROMPT_TYPE_CONFIGS.get(prompt_type)
    return config.get("enabled", False) if config else False


def validate_prompt_type(prompt_type: str) -> str:
    """
    Validates a prompt type and returns it if valid, or 'basic' as fallback.
    
    Args:
        prompt_type: String of the type to validate
    
    Returns:
        Valid prompt type string (original or 'basic' as fallback)
    """
    if not prompt_type:
        return "basic"
    
    # Check if type exists
    if prompt_type not in PROMPT_TYPE_CONFIGS:
        print(f"Warning: Unknown prompt type '{prompt_type}', defaulting to 'basic'")
        return "basic"
    
    # Check if type is enabled
    if not is_prompt_type_enabled(prompt_type):
        print(f"Warning: Prompt type '{prompt_type}' is not enabled, defaulting to 'basic'")
        return "basic"
    
    return prompt_type

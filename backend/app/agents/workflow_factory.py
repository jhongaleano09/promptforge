"""
Workflow Factory Module

Factory Pattern implementation for selecting the appropriate workflow (graph)
based on the prompt type selected by the user.

This allows for easy extension and addition of new prompt types without
modifying existing code.
"""

from typing import Any
from app.core.prompt_types import (
    PromptType, 
    get_prompt_type_config, 
    is_prompt_type_enabled,
    get_enabled_prompt_types
)
from app.agents.graph import get_graph as get_basic_graph

# Future workflow imports (will be uncommented when implemented):
# from app.agents.system_prompt_graph import get_graph as get_system_prompt_graph
# from app.agents.image_prompt_graph import get_graph as get_image_prompt_graph
# from app.agents.additional_prompt_graph import get_graph as get_additional_prompt_graph


def get_workflow_graph(prompt_type: str, checkpointer=None) -> Any:
    """
    Factory Pattern: Returns the appropriate workflow (LangGraph graph)
    based on the selected prompt type.
    
    Args:
        prompt_type: String of the prompt type ('basic', 'system', 'image', 'additional')
        checkpointer: LangGraph checkpointer for state persistence
    
    Returns:
        Compiled LangGraph workflow object.
    
    Raises:
        ValueError: If the prompt type is not enabled.
        ValueError: If the workflow for the type doesn't exist.
    """
    # Get prompt type configuration
    try:
        config = get_prompt_type_config(prompt_type)
    except ValueError as e:
        print(f"Error: {e}. Falling back to 'basic' workflow.")
        return get_basic_graph(checkpointer)
    
    # Validate that the type is enabled
    if not config.get("enabled", False):
        enabled_types = get_enabled_prompt_types()
        print(
            f"Warning: Prompt type '{prompt_type}' is not enabled. "
            f"Enabled types: {enabled_types}. Falling back to 'basic' workflow."
        )
        return get_basic_graph(checkpointer)
    
    # Get the workflow name to use
    workflow_name = config.get("workflow_graph")
    
    # Factory: Import and return the corresponding workflow
    # This allows future extension without modifying existing code
    
    # Basic workflow (already implemented)
    if workflow_name == "basic_workflow":
        return get_basic_graph(checkpointer)
    
    # Specific workflows (will be implemented in phases 8.6, 8.7, 8.8)
    elif workflow_name == "system_prompt_workflow":
        # Will be implemented in Phase 8.6
        try:
            from app.agents.system_prompt_graph import get_graph as get_system_prompt_graph
            return get_system_prompt_graph(checkpointer)
        except ImportError:
            print(
                f"Warning: System prompt workflow is not yet implemented. "
                "Check Phase 8.6 for implementation details. Falling back to 'basic' workflow."
            )
            return get_basic_graph(checkpointer)
    
    elif workflow_name == "image_prompt_workflow":
        # Will be implemented in Phase 8.7
        try:
            from app.agents.image_prompt_graph import get_graph as get_image_prompt_graph
            return get_image_prompt_graph(checkpointer)
        except ImportError:
            print(
                f"Warning: Image prompt workflow is not yet implemented. "
                "Check Phase 8.7 for implementation details. Falling back to 'basic' workflow."
            )
            return get_basic_graph(checkpointer)
    
    elif workflow_name == "additional_prompt_workflow":
        # Will be implemented in Phase 8.8
        try:
            from app.agents.additional_prompt_graph import get_graph as get_additional_prompt_graph
            return get_additional_prompt_graph(checkpointer)
        except ImportError:
            print(
                f"Warning: Additional prompt workflow is not yet implemented. "
                "Check Phase 8.8 for implementation details. Falling back to 'basic' workflow."
            )
            return get_basic_graph(checkpointer)
    
    else:
        # Fallback: Unrecognized workflow
        # Use basic workflow by default
        print(
            f"Warning: Workflow '{workflow_name}' not recognized. "
            "Falling back to 'basic' workflow."
        )
        return get_basic_graph(checkpointer)


def get_available_workflows() -> list:
    """
    Returns list of available workflows with their types.
    
    Returns:
        List of dicts with information about each available workflow.
    """
    available = []
    
    for ptype in get_enabled_prompt_types():
        config = get_prompt_type_config(ptype)
        workflow_name = config.get("workflow_graph")
        
        # Check if the workflow is implemented
        implemented = True
        if workflow_name in ["system_prompt_workflow", "image_prompt_workflow", "additional_prompt_workflow"]:
            # These workflows will be verified when used
            # For now, assume they are not implemented
            implemented = workflow_name == "basic_workflow"
        
        available.append({
            "prompt_type": ptype,
            "workflow_name": workflow_name,
            "implemented": implemented,
            "config": config
        })
    
    return available

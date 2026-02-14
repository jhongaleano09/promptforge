from typing import TypedDict, List, Dict, Optional, Any
from langchain_core.messages import BaseMessage
import operator
from typing import Annotated

class PromptState(TypedDict):
    """
    State definition for the PromptForge LangGraph workflow.
    """
    user_input: str
    requirements: Dict[str, Any]
    clarification_dialogue: Annotated[List[BaseMessage], operator.add]
    generated_variants: List[Dict[str, Any]]  # [ {id: 'A', content: '...'}, ... ]
    evaluations: Dict[str, Any]  # { 'A': {score: 9, ...} }
    selected_variant: Optional[str]
    # 'messages' is reserved for the graph's internal message history if using MessageGraph,
    # but we are using StateGraph with custom state, so we define what we need.
    messages: Annotated[List[BaseMessage], operator.add]

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, AIMessage

from app.agents.state import PromptState
from app.agents.nodes import clarify_node, generate_node, evaluate_node

# --- Conditional Logic ---

def should_continue(state: PromptState) -> Literal["generate", END]:
    """
    Decides if we should proceed to generation or wait for user input.
    """
    requirements = state.get("requirements", {})
    questions = requirements.get("questions", [])
    
    # If the clarifier generated questions, we stop to let the user answer.
    # The last message in 'messages' should be the AIMessage with questions.
    if questions:
        return END
    
    # If no questions, we proceed to generation.
    return "generate"

# --- Graph Construction ---

workflow = StateGraph(PromptState)

# Add Nodes
workflow.add_node("clarify", clarify_node)
workflow.add_node("generate", generate_node)
workflow.add_node("evaluate", evaluate_node)

# Add Edges
workflow.set_entry_point("clarify")

workflow.add_conditional_edges(
    "clarify",
    should_continue,
    {
        "generate": "generate",
        END: END
    }
)

workflow.add_edge("generate", "evaluate")
workflow.add_edge("evaluate", END)

# --- Compilation ---
# We need to provide a checkpointer for persistence.
# This will be initialized in the API layer or app startup to avoid global connection issues.
# For now, we return the builder or a factory function.

def get_graph(checkpointer=None):
    return workflow.compile(checkpointer=checkpointer)

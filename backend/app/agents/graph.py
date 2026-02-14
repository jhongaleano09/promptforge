from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, AIMessage

from app.agents.state import PromptState
from app.agents.nodes import clarify_node, generate_node, evaluate_node, judge_node, refiner_node

# --- Conditional Logic ---

def router(state: PromptState) -> Literal["clarify", "refine"]:
    """
    Decides the starting point based on state.
    """
    # If a variant is selected, we are in refinement mode.
    if state.get("selected_variant"):
        return "refine"
    
    return "clarify"

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
workflow.add_node("judge", judge_node)
workflow.add_node("refine", refiner_node)

# Add Edges
# We use a conditional entry point to handle refinement loops vs new starts
workflow.set_conditional_entry_point(
    router,
    {
        "clarify": "clarify",
        "refine": "refine"
    }
)

workflow.add_conditional_edges(
    "clarify",
    should_continue,
    {
        "generate": "generate",
        END: END
    }
)

workflow.add_edge("generate", "evaluate")
workflow.add_edge("evaluate", "judge") # Auto-judge after evaluation
workflow.add_edge("judge", END) # Wait for user action

# Refinement Loop
workflow.add_edge("refine", "evaluate") # After refining, re-evaluate the new variants

# --- Compilation ---
def get_graph(checkpointer=None):
    return workflow.compile(checkpointer=checkpointer)

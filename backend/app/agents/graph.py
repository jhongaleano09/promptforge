from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, AIMessage
import logging

logger = logging.getLogger(__name__)

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
    user_answers = requirements.get("user_answers", [])
    
    # ✅ FIX: Si el usuario ya respondió, proceder a generación
    # El usuario ya proporcionó la información necesaria
    if user_answers:
        logger.info("[SHOULD_CONTINUE] Usuario respondió a preguntas. Procediendo a generate...")
        return "generate"
    
    # Si hay preguntas y NO hay respuestas, esperar al usuario
    if questions and not user_answers:
        logger.info("[SHOULD_CONTINUE] Hay preguntas sin respuestas. Esperando al usuario...")
        return END
    
    # Si no hay preguntas (primera ejecución o ya clarificado), proceder a generación
    logger.info("[SHOULD_CONTINUE] No hay preguntas pendientes. Procediendo a generate...")
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

import uuid
import json
from fastapi import APIRouter, HTTPException, BackgroundTasks
from langchain_core.messages import HumanMessage, AIMessage

from app.api.schemas import WorkflowStartRequest, WorkflowAnswerRequest, WorkflowResponse
from app.core.workflow_manager import workflow_manager

router = APIRouter()

async def format_response(thread_id: str, state: dict) -> WorkflowResponse:
    requirements = state.get("requirements", {})
    questions = requirements.get("questions", [])
    variants = state.get("generated_variants", [])
    evaluations = state.get("evaluations", {})
    
    status = "clarifying"
    if variants:
        status = "completed"
    elif not questions and not variants:
        # Should not happen ideally unless error or initial state
        status = "processing"

    # Extract clean questions list
    # If questions are in JSON format inside the dictionary
    clean_questions = []
    if questions:
        clean_questions = questions

    # Get last message for UI context
    last_msg = ""
    messages = state.get("messages", []) # LangGraph internal messages if any
    # Or clarification_dialogue
    dialogue = state.get("clarification_dialogue", [])
    if dialogue:
        last_m = dialogue[-1]
        if isinstance(last_m, AIMessage):
             last_msg = last_m.content

    return WorkflowResponse(
        thread_id=thread_id,
        status=status,
        message=last_msg,
        questions=clean_questions,
        variants=variants,
        evaluations=evaluations
    )

@router.post("/start", response_model=WorkflowResponse)
async def start_workflow(request: WorkflowStartRequest):
    thread_id = str(uuid.uuid4())
    manager = await workflow_manager.get_instance()
    graph = await manager.get_graph_runnable()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial input
    initial_state = {
        "user_input": request.user_input,
        "clarification_dialogue": [], # Start empty
        "requirements": {},
        "generated_variants": [],
        "evaluations": {}
    }
    
    # Run the graph
    # It will run until it hits END (either because of questions or completion)
    final_state = await graph.ainvoke(initial_state, config)
    
    return await format_response(thread_id, final_state)

@router.post("/{thread_id}/answer", response_model=WorkflowResponse)
async def answer_clarification(thread_id: str, request: WorkflowAnswerRequest):
    manager = await workflow_manager.get_instance()
    graph = await manager.get_graph_runnable()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # We resume by sending the user's answer.
    # Because clarification_dialogue has operator.add, this appends.
    # The graph entry point 'clarify' will run again, seeing the updated history.
    input_delta = {
        "clarification_dialogue": [HumanMessage(content=request.answer)]
    }
    
    final_state = await graph.ainvoke(input_delta, config)
    
    return await format_response(thread_id, final_state)

@router.get("/{thread_id}/state", response_model=WorkflowResponse)
async def get_workflow_state(thread_id: str):
    manager = await workflow_manager.get_instance()
    graph = await manager.get_graph_runnable()
    
    config = {"configurable": {"thread_id": thread_id}}
    state = await graph.aget_state(config)
    
    if not state.values:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    return await format_response(thread_id, state.values)

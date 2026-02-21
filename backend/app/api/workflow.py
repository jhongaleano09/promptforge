import uuid
import json
import asyncio
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage

from app.api.schemas import WorkflowStartRequest, WorkflowAnswerRequest, WorkflowResponse
from app.core.workflow_manager import workflow_manager
from app.agents.workflow_factory import get_workflow_graph
from app.core.prompt_types import validate_prompt_type

logger = logging.getLogger(__name__)

router = APIRouter()

async def format_response(thread_id: str, state: dict) -> WorkflowResponse:
    """Formatea el estado del grafo en una respuesta para el frontend."""
    # Log state for debugging
    logger.info(f"format_response called with state type: {type(state)}")
    
    if isinstance(state, list):
        logger.warning(f"State is a list! Length: {len(state)}. Content sample: {str(state)[:500]}")
        # Intentar recuperar si es una lista de mensajes
        # Esto puede pasar si LangGraph devuelve mensajes directamente
        return WorkflowResponse(
            thread_id=thread_id,
            status="error",
            message="Internal Error: State format unexpected (list). See logs.",
            questions=[],
            variants=[],
            evaluations={}
        )
    
    if not isinstance(state, dict):
        logger.error(f"State is neither dict nor list! Type: {type(state)}")
        return WorkflowResponse(
            thread_id=thread_id,
            status="error",
            message="Internal Error: State format invalid. See logs.",
            questions=[],
            variants=[],
            evaluations={}
        )

    logger.info(f"state keys: {list(state.keys())}")

    # Handle different formats for requirements
    requirements = state.get("requirements", {})
    if isinstance(requirements, list):
        # If requirements is a list (old format), convert to dict
        logger.warning(f"requirements is a list, converting to dict. Length: {len(requirements)}")
        requirements = {"has_questions": True, "questions": requirements}
    elif not isinstance(requirements, dict):
        logger.error(f"requirements is neither list nor dict, type: {type(requirements)}")
        requirements = {}

    questions = requirements.get("questions", []) if isinstance(requirements, dict) else []
    variants = state.get("generated_variants", [])
    evaluations = state.get("evaluations", {})

    status = "clarifying"
    if variants:
        status = "completed"
    elif not questions and not variants:
        status = "processing"

    # Extract clean questions list
    clean_questions = questions if isinstance(questions, list) else []

    # Get last message for UI context
    last_msg = ""
    dialogue = state.get("clarification_dialogue", [])
    if dialogue and isinstance(dialogue, list) and len(dialogue) > 0:
        last_m = dialogue[-1]
        if isinstance(last_m, AIMessage):
             last_msg = last_m.content
        elif isinstance(last_m, dict) and "content" in last_m:
             last_msg = last_m["content"]

    logger.info(f"format_response returning: status={status}, questions_len={len(clean_questions)}, variants_len={len(variants)}")

    return WorkflowResponse(
        thread_id=thread_id,
        status=status,
        message=last_msg,
        questions=clean_questions,
        variants=variants,
        evaluations=evaluations
    )

async def event_generator(graph, input_state, config):
    """
    Generador de eventos usando astream con stream_mode='values'.
    Este enfoque es más confiable que astream_events.
    """
    thread_id = config["configurable"]["thread_id"]
    yield f"event: metadata\ndata: {json.dumps({'thread_id': thread_id})}\n\n"
    
    try:
        # Usar astream con stream_mode='values' para obtener el estado completo en cada paso
        async for state in graph.astream(input_state, config, stream_mode="values"):
            logger.info(f"Stream received state type: {type(state)}, keys: {list(state.keys()) if isinstance(state, dict) else 'N/A'}")
            
            if isinstance(state, dict):
                # Determinar el estado actual basado en las claves presentes
                requirements = state.get("requirements", {})
                has_questions = False
                if isinstance(requirements, dict):
                    has_questions = requirements.get("has_questions", False) or bool(requirements.get("questions", []))
                
                variants = state.get("generated_variants", [])
                
                # Enviar evento de status basado en el estado actual
                if has_questions and not variants:
                    yield f"event: status\ndata: {json.dumps({'status': 'clarifying'})}\n\n"
                elif variants:
                    yield f"event: status\ndata: {json.dumps({'status': 'completed'})}\n\n"
                else:
                    yield f"event: status\ndata: {json.dumps({'status': 'processing'})}\n\n"
                
                # Formatear y enviar la actualización del estado
                try:
                    response_obj = await format_response(thread_id, state)
                    yield f"event: update\ndata: {response_obj.model_dump_json()}\n\n"
                except Exception as e:
                    logger.error(f"Error formatting response: {e}")
                    yield f"event: error\ndata: {json.dumps({'detail': f'Format error: {str(e)}'})}\n\n"
            else:
                logger.warning(f"Received non-dict state: {type(state)}")
                
    except Exception as e:
        logger.error(f"Streaming Error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        yield f"event: error\ndata: {json.dumps({'detail': str(e)})}\n\n"

@router.post("/stream/start")
async def start_workflow_stream(request: WorkflowStartRequest):
    thread_id = str(uuid.uuid4())
    manager = await workflow_manager.get_instance()
    
    # Validate and get prompt type (with fallback to 'basic')
    prompt_type = validate_prompt_type(request.prompt_type)
    
    # Get the appropriate workflow graph using factory pattern
    checkpointer = await manager.get_checkpointer()
    graph = get_workflow_graph(prompt_type, checkpointer=checkpointer)

    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "user_input": request.user_input,
        "selected_provider": request.provider,
        "selected_model": request.model,
        "prompt_type": prompt_type,  # Add prompt type to state
        "clarification_dialogue": [],
        "requirements": {},
        "generated_variants": [],
        "evaluations": {}
    }

    return StreamingResponse(
        event_generator(graph, initial_state, config),
        media_type="text/event-stream"
    )

@router.post("/stream/{thread_id}/answer")
async def answer_clarification_stream(thread_id: str, request: WorkflowAnswerRequest):
    manager = await workflow_manager.get_instance()
    checkpointer = await manager.get_checkpointer()
    
    # Get current state to retrieve prompt_type
    config = {"configurable": {"thread_id": thread_id}}
    temp_graph = get_workflow_graph("basic", checkpointer=checkpointer)  # Use basic to get state
    state = await temp_graph.aget_state(config)
    
    # Extract prompt_type from state, default to 'basic' if not found
    prompt_type = state.values.get("prompt_type", "basic") if state.values else "basic"
    prompt_type = validate_prompt_type(prompt_type)
    
    # Get the appropriate workflow graph
    graph = get_workflow_graph(prompt_type, checkpointer=checkpointer)
    
    input_delta = {
        "clarification_dialogue": [HumanMessage(content=request.answer)]
    }
    
    return StreamingResponse(
        event_generator(graph, input_delta, config),
        media_type="text/event-stream"
    )

@router.post("/start", response_model=WorkflowResponse)
async def start_workflow(request: WorkflowStartRequest):
    thread_id = str(uuid.uuid4())
    manager = await workflow_manager.get_instance()
    checkpointer = await manager.get_checkpointer()
    
    # Validate and get prompt type
    prompt_type = validate_prompt_type(request.prompt_type)
    graph = get_workflow_graph(prompt_type, checkpointer=checkpointer)
    
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "user_input": request.user_input,
        "selected_provider": request.provider,
        "prompt_type": prompt_type,
        "clarification_dialogue": [],
        "requirements": {},
        "generated_variants": [],
        "evaluations": {}
    }
    
    final_state = await graph.ainvoke(initial_state, config)
    
    return await format_response(thread_id, final_state)

@router.post("/{thread_id}/answer", response_model=WorkflowResponse)
async def answer_clarification(thread_id: str, request: WorkflowAnswerRequest):
    manager = await workflow_manager.get_instance()
    checkpointer = await manager.get_checkpointer()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Get current state to retrieve prompt_type
    temp_graph = get_workflow_graph("basic", checkpointer=checkpointer)
    state = await temp_graph.aget_state(config)
    prompt_type = state.values.get("prompt_type", "basic") if state.values else "basic"
    prompt_type = validate_prompt_type(prompt_type)
    
    # Get the appropriate workflow graph
    graph = get_workflow_graph(prompt_type, checkpointer=checkpointer)
    
    input_delta = {
        "clarification_dialogue": [HumanMessage(content=request.answer)]
    }
    
    final_state = await graph.ainvoke(input_delta, config)
    
    return await format_response(thread_id, final_state)

@router.get("/{thread_id}/state", response_model=WorkflowResponse)
async def get_workflow_state(thread_id: str):
    manager = await workflow_manager.get_instance()
    checkpointer = await manager.get_checkpointer()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Get current state to retrieve prompt_type
    temp_graph = get_workflow_graph("basic", checkpointer=checkpointer)
    state = await temp_graph.aget_state(config)
    
    if not state.values:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    return await format_response(thread_id, state.values)

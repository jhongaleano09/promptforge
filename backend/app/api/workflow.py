import uuid
import json
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
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

async def event_generator(graph, input_state, config):
    thread_id = config["configurable"]["thread_id"]
    yield f"event: metadata\ndata: {json.dumps({'thread_id': thread_id})}\n\n"
    
    try:
        async for event in graph.astream_events(input_state, config, version="v1"):
            kind = event["event"]
            
            # Token Streaming
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if hasattr(chunk, "content") and chunk.content:
                     yield f"event: token\ndata: {json.dumps({'content': chunk.content})}\n\n"

            # Node Transitions
            elif kind == "on_chain_start":
                name = event["name"]
                if name in ["clarify", "generate", "evaluate"]:
                    yield f"event: status\ndata: {json.dumps({'status': name})}\n\n"
            
            # Final Output
            elif kind == "on_chain_end" and event["name"] == "LangGraph":
                final_state = event["data"]["output"]
                if final_state: # Ensure we have output
                    response_obj = await format_response(thread_id, final_state)
                    yield f"event: update\ndata: {response_obj.model_dump_json()}\n\n"
                
    except Exception as e:
        # Log error in console for debug
        print(f"Streaming Error: {e}")
        yield f"event: error\ndata: {json.dumps({'detail': str(e)})}\n\n"

@router.post("/stream/start")
async def start_workflow_stream(request: WorkflowStartRequest):
    thread_id = str(uuid.uuid4())
    manager = await workflow_manager.get_instance()
    graph = await manager.get_graph_runnable()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "user_input": request.user_input,
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
    graph = await manager.get_graph_runnable()
    
    config = {"configurable": {"thread_id": thread_id}}
    
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

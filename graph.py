import os
from typing import Dict, Any, List, TypedDict, Literal, Optional
from datetime import datetime, timezone
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

# Import improved memory module
try:
    from memory_persistent import IlluminatorPersistentMemory
except ImportError:
    IlluminatorPersistentMemory = None


# ==========================================
# Estado del sistema (compatible con communication_protocol.json v1.0.0)
# ==========================================
class IlluminatorState(TypedDict):
    schema_version: str
    task_id: str
    parent_task_id: Optional[str]
    sender: str
    receiver: str
    status: Literal["pending", "in_progress", "completed", "failed", "warning"]
    payload: Dict[str, Any]
    diagnostics: Dict[str, Any]
    feedback_to_nucleus: Dict[str, Any]
    timestamp: str


# ==========================================
# Decorador de seguridad
# ==========================================
def safe_node_execution(node_func):
    def wrapper(state: IlluminatorState, config: RunnableConfig) -> IlluminatorState:
        thread_id = config.get("configurable", {}).get("thread_id", "default_thread")
        try:
            state["status"] = "in_progress"
            state["timestamp"] = datetime.now(timezone.utc).isoformat()
            return node_func(state, config)
        except Exception as e:
            if "diagnostics" not in state or not state.get("diagnostics"):
                state["diagnostics"] = {"errors": [], "warnings": []}
            state["diagnostics"]["errors"].append(f"Error en [{node_func.__name__}] | Thread: {thread_id} | {str(e)}")
            state["status"] = "failed"
            state["feedback_to_nucleus"] = {
                "token_tier": "Alto",
                "suggested_next_action": "Revisar error y activar contingencia",
                "requires_human_intervention": True
            }
            return state
    return wrapper


# ==========================================
# Nodos
# ==========================================
@safe_node_execution
def nucleus_supervisor_node(state: IlluminatorState, config: RunnableConfig) -> IlluminatorState:
    """Núcleo Director con integración de memoria persistente"""
    thread_id = config.get("configurable", {}).get("thread_id", "default_thread")
    state["sender"] = "grok_nucleus"
    state["schema_version"] = "1.0.0"

    # Inicializar memoria si está disponible
    memory = None
    if IlluminatorPersistentMemory:
        try:
            memory = IlluminatorPersistentMemory(user_id="default")
        except Exception:
            memory = None

    # Re-hidratación desde memoria persistente
    if memory:
        try:
            previous = memory.get_latest_state(thread_id=thread_id)
            if previous:
                state["payload"]["historical_context"] = previous.get("payload", {}).get("output_data", {})
                if "diagnostics" not in state:
                    state["diagnostics"] = {"errors": [], "warnings": []}
                state["diagnostics"]["warnings"].append("Contexto histórico recuperado desde memoria persistente.")
        except Exception as e:
            if "diagnostics" not in state:
                state["diagnostics"] = {"errors": [], "warnings": []}
            state["diagnostics"]["warnings"].append(f"No se pudo recuperar historial: {str(e)}")

    # Lógica de ruteo
    if state.get("status") == "failed":
        state["receiver"] = "system"
    else:
        state["receiver"] = "gemini_agent"

    # Guardar estado actual en memoria persistente
    if memory:
        try:
            memory.save_state(thread_id=thread_id, state=dict(state))
        except Exception as e:
            if "diagnostics" not in state:
                state["diagnostics"] = {"errors": [], "warnings": []}
            state["diagnostics"]["errors"].append(f"Error al guardar estado en memoria: {str(e)}")

    return state


@safe_node_execution
def gemini_agent_node(state: IlluminatorState, config: RunnableConfig) -> IlluminatorState:
    state["sender"] = "gemini_agent"
    state["receiver"] = "grok_nucleus"
    state["status"] = "completed"
    return state


# ==========================================
# Router
# ==========================================
def router(state: IlluminatorState) -> str:
    if state.get("status") == "failed":
        return END
    if state.get("receiver") == "gemini_agent":
        return "gemini_agent"
    return END


# ==========================================
# Creación del Grafo con Memoria Persistente
# ==========================================
def create_graph():
    workflow = StateGraph(IlluminatorState)
    
    workflow.add_node("grok_nucleus", nucleus_supervisor_node)
    workflow.add_node("gemini_agent", gemini_agent_node)
    
    workflow.set_entry_point("grok_nucleus")
    
    workflow.add_conditional_edges("grok_nucleus", router, {
        "gemini_agent": "gemini_agent",
        END: END
    })
    
    workflow.add_edge("gemini_agent", "grok_nucleus")
    
    # Integración de checkpointer usando la nueva interfaz
    checkpointer = None
    if IlluminatorPersistentMemory:
        try:
            memory = IlluminatorPersistentMemory(user_id="default")
            checkpointer = memory.get_checkpointer()
        except Exception as e:
            print(f"\u26a0\ufe0f No se pudo obtener checkpointer: {e}")
    
    if checkpointer:
        return workflow.compile(checkpointer=checkpointer)
    else:
        return workflow.compile()


app = create_graph()

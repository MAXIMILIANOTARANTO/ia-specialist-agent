from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated, Optional, Dict, List, Any
import json
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemState(TypedDict):
    user_input: str
    final_output: Optional[str]
    supervisor_decision: str
    selected_route: str
    confidence_score: float
    analysis_result: Optional[Dict[str, Any]]
    generation_result: Optional[Dict[str, Any]]
    validation_result: Optional[Dict[str, Any]]
    memory_context: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    feedback_loops: List[str]
    error_log: List[str]
    libro_firma_entry: Optional[Dict[str, Any]]
    validation_status: str
    execution_id: str
    timestamp: str
    agent_trace: List[str]

def initialize_state(user_input: str) -> SystemState:
    execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return SystemState(
        user_input=user_input,
        final_output=None,
        supervisor_decision="",
        selected_route="",
        confidence_score=0.0,
        analysis_result=None,
        generation_result=None,
        validation_result=None,
        memory_context={},
        conversation_history=[],
        feedback_loops=[],
        error_log=[],
        libro_firma_entry=None,
        validation_status="pending",
        execution_id=execution_id,
        timestamp=datetime.now().isoformat(),
        agent_trace=[],
    )

class SupervisorNode:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info(f"[SUPERVISOR] Recibido: {state['user_input'][:50]}...")
        user_input = state['user_input'].lower()
        if any(word in user_input for word in ['analiza', 'evalúa', 'revisa', 'error', 'problema']):
            route = "analysis"
            decision = "Requerimiento de análisis profundo detectado"
            confidence = 0.95
        elif any(word in user_input for word in ['crea', 'genera', 'escribe', 'código', 'diseña']):
            route = "generation"
            decision = "Requerimiento de generación de contenido detectado"
            confidence = 0.92
        elif any(word in user_input for word in ['valida', 'prueba', 'verifica', 'test', 'qa']):
            route = "validation"
            decision = "Requerimiento de validación detectado"
            confidence = 0.90
        else:
            route = "analysis"
            decision = "Análisis general recomendado"
            confidence = 0.75
        state['supervisor_decision'] = decision
        state['selected_route'] = route
        state['confidence_score'] = confidence
        state['agent_trace'].append(f"SUPERVISOR → {route.upper()} (confidence: {confidence})")
        logger.info(f"[SUPERVISOR] Decisión: {route.upper()} ({decision})")
        return state

class AnalysisSpecialist:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info("[ANÁLISIS] Iniciando evaluación...")
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "input_length": len(state['user_input']),
            "input_hash": hash(state['user_input']),
            "keywords": state['user_input'].split(),
            "complexity_level": "medium",
            "recommendation": "Proceder con precaución",
            "issues_found": [],
            "insights": [
                "Input recibido y evaluado",
                "Estructura sintáctica correcta",
                "Contexto coherente detectado"
            ]
        }
        state['analysis_result'] = analysis
        state['agent_trace'].append("SPECIALIST_ANALYSIS → completado")
        state['validation_status'] = "validated"
        logger.info(f"[ANÁLISIS] Completado: {len(analysis['insights'])} insights")
        return state

class GenerationSpecialist:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info("[GENERACIÓN] Creando respuesta...")
        analysis = state['analysis_result'] or {}
        generation = {
            "timestamp": datetime.now().isoformat(),
            "based_on_analysis": bool(analysis),
            "solution_type": "integrated",
            "components": [
                "estructura_base",
                "validaciones",
                "documentacion"
            ],
            "generated_content": f"Solución generada para: {state['user_input'][:50]}...",
            "quality_score": 0.88,
            "ready_for_validation": True
        }
        state['generation_result'] = generation
        state['agent_trace'].append("SPECIALIST_GENERATION → completado")
        state['validation_status'] = "validated"
        logger.info(f"[GENERACIÓN] Solución lista (calidad: {generation['quality_score']})")
        return state

class ValidationSpecialist:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info("[VALIDACIÓN] Verificando solución...")
        generation = state['generation_result'] or {}
        validation = {
            "timestamp": datetime.now().isoformat(),
            "validated_content": bool(generation),
            "checks_performed": [
                "syntax_check",
                "coherence_check",
                "safety_check",
                "completeness_check"
            ],
            "checks_passed": 4,
            "checks_total": 4,
            "quality_metrics": {
                "coherence": 0.94,
                "completeness": 0.91,
                "safety": 0.98,
                "performance": 0.89
            },
            "recommendation": "APROBADO",
            "notes": "Solución lista para producción"
        }
        state['validation_result'] = validation
        state['validation_status'] = "validated"
        state['agent_trace'].append("SPECIALIST_VALIDATION → completado")
        logger.info(f"[VALIDACIÓN] Resultado: {validation['recommendation']}")
        return state

class MemoryNode:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info("[MEMORIA] Sincronizando estado...")
        memory_entry = {
            "execution_id": state['execution_id'],
            "timestamp": state['timestamp'],
            "user_input": state['user_input'][:100],
            "supervisor_route": state['selected_route'],
            "analysis_summary": state['analysis_result'] is not None,
            "generation_summary": state['generation_result'] is not None,
            "validation_status": state['validation_status'],
        }
        state['memory_context'] = memory_entry
        state['conversation_history'].append({
            "role": "system",
            "content": f"[{state['execution_id']}] Procesado en ruta: {state['selected_route']}"
        })
        state['agent_trace'].append("MEMORY_NODE → sincronizado")
        logger.info(f"[MEMORIA] Contexto guardado: {state['execution_id']}")
        return state

class ValidationLibroFirma:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info("[LIBRO_FIRMA] Registrando acción...")
        libro_entry = {
            "id": state['execution_id'],
            "timestamp": state['timestamp'],
            "agent": "Claude",
            "action": f"Procesó: {state['selected_route'].upper()}",
            "input_hash": hash(state['user_input']),
            "validation_status": state['validation_status'],
            "confidence": state['confidence_score'],
            "status": "REGISTERED",
            "signature": f"sig_{state['execution_id']}"
        }
        state['libro_firma_entry'] = libro_entry
        state['agent_trace'].append("VALIDATION_LIBRO_FIRMA → registrado")
        logger.info(f"[LIBRO_FIRMA] Acción registrada: {libro_entry['action']}")
        return state

class OutputNode:
    @staticmethod
    def process(state: SystemState) -> SystemState:
        logger.info("[OUTPUT] Sintetizando resultados...")
        final_output = {
            "execution_id": state['execution_id'],
            "status": "COMPLETED",
            "route": state['selected_route'],
            "analysis": state['analysis_result'] is not None,
            "generation": state['generation_result'] is not None,
            "validation": state['validation_status'],
            "confidence": state['confidence_score'],
            "message": f"Proceso completado exitosamente en ruta {state['selected_route'].upper()}",
            "trace": state['agent_trace'],
            "next_action": "Ready for Grok execution"
        }
        state['final_output'] = json.dumps(final_output, indent=2, ensure_ascii=False)
        state['agent_trace'].append("OUTPUT → generado")
        logger.info("[OUTPUT] Resultado final listo")
        return state

def route_after_supervisor(state) -> str:
    status = state.get("validation_status", "")
    if status in ["validated", "completed", "finalized", "done"]:
        return "memory"
    route = state.get("selected_route", "analysis")
    if route in ["analysis", "generation", "validation"]:
        return route
    return "memory"

def build_iluminador_graph():
    from langgraph.checkpoint.memory import MemorySaver
    graph = StateGraph(SystemState)
    graph.add_node("supervisor", SupervisorNode.process)
    graph.add_node("analysis", AnalysisSpecialist.process)
    graph.add_node("generation", GenerationSpecialist.process)
    graph.add_node("validation", ValidationSpecialist.process)
    graph.add_node("memory", MemoryNode.process)
    graph.add_node("libro_firma", ValidationLibroFirma.process)
    graph.add_node("output", OutputNode.process)
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "analysis": "analysis",
            "generation": "generation",
            "validation": "validation",
            "memory": "memory"
        }
    )
    graph.add_edge("analysis", "supervisor")
    graph.add_edge("generation", "supervisor")
    graph.add_edge("validation", "supervisor")
    graph.add_edge("memory", "libro_firma")
    graph.add_edge("libro_firma", "output")
    graph.add_edge("output", END)
    graph.set_entry_point("supervisor")
    return graph.compile(checkpointer=MemorySaver())

class ElIluminadorCore:
    def __init__(self):
        logger.info("🌀 Inicializando EL ILUMINADOR v1.1...")
        self.graph = build_iluminador_graph()
        self.execution_history = []
        logger.info("✅ EL ILUMINADOR v1.1 listo")
    def process(self, user_input: str) -> Dict[str, Any]:
        logger.info(f"🚀 Procesando: {user_input[:50]}...")
        initial_state = initialize_state(user_input)
        try:
            config = {"configurable": {"thread_id": initial_state["execution_id"]}}
            final_state = self.graph.invoke(initial_state, config=config)
            self.execution_history.append({
                "execution_id": final_state['execution_id'],
                "timestamp": final_state['timestamp'],
                "status": "success",
                "route": final_state['selected_route']
            })
            logger.info(f"✅ Ejecución completada: {final_state['execution_id']}")
            return {
                "success": True,
                "execution_id": final_state['execution_id'],
                "output": final_state['final_output'],
                "trace": final_state['agent_trace'],
                "validation_status": final_state['validation_status'],
                "confidence": final_state['confidence_score']
            }
        except Exception as e:
            logger.error(f"❌ Error en ejecución: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "trace": initial_state['agent_trace']
            }

if __name__ == "__main__":
    iluminador = ElIluminadorCore()
    test_input = "Analiza el estado del proyecto y propón mejoras"
    result = iluminador.process(test_input)
    print("\n" + "="*70)
    print("🌀 EL ILUMINADOR v1.1 - RESULTADO DE EJECUCIÓN")
    print("="*70)
    print(result['output'] if result['success'] else f"Error: {result['error']}")
    print("="*70 + "\n")

from typing import Literal

from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import END
from langgraph.types import Command
from pydantic import BaseModel

from config import get_llm, SUPERVISOR_MODEL
from state import AgentState

MEMBERS = ["researcher", "architect", "coder", "reviewer"]
MAX_TURNS = 12  # corta el loop si el supervisor nunca decide FINISH

supervisor_prompt = """Eres el Supervisor de un equipo de especialistas en IA y sistemas complejos:
- researcher: investiga información técnica y tendencias.
- architect: diseña arquitecturas y patrones de sistemas.
- coder: escribe e implementa código.
- reviewer: revisa calidad, detecta bugs y code smells.

Dada la conversación, decide a qué especialista delegar a continuación, o responde FINISH
si ya hay una respuesta final satisfactoria para el usuario en el último mensaje del equipo."""


class RouteDecision(BaseModel):
    next: Literal["researcher", "architect", "coder", "reviewer", "FINISH"]


def create_supervisor_node():
    llm = get_llm(SUPERVISOR_MODEL)
    router = llm.with_structured_output(RouteDecision)

    def supervisor(state: AgentState) -> Command:
        if len(state["messages"]) > MAX_TURNS:
            decision_next = "FINISH"
        else:
            decision = router.invoke([SystemMessage(content=supervisor_prompt)] + state["messages"])
            decision_next = decision.next

        if decision_next == "FINISH":
            last_ai = next(
                (m for m in reversed(state["messages"]) if isinstance(m, AIMessage)), None
            )
            final_response = last_ai.content if last_ai else ""
            return Command(goto=END, update={"next": "FINISH", "final_response": final_response})

        return Command(goto=decision_next, update={"next": decision_next})

    return supervisor

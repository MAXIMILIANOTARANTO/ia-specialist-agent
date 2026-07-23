from langgraph.graph import StateGraph, START, END

from agent_tools import get_search_tool
from agents.architect import create_architect_agent
from agents.coder import create_coder_agent
from agents.researcher import create_researcher_agent
from agents.reviewer import create_reviewer_agent
from agents.supervisor import create_supervisor_node
from state import AgentState


def _specialist_node(agent_graph):
    """Envuelve un agente prebuilt (create_react_agent) como nodo del supervisor,
    devolviendo solo los mensajes nuevos que generó (evita reprocesar el historial)."""

    def node(state: AgentState):
        input_messages = state["messages"]
        result = agent_graph.invoke({"messages": input_messages})
        new_messages = result["messages"][len(input_messages):]
        return {"messages": new_messages}

    return node


def create_graph(checkpointer=None, store=None):
    tools = [get_search_tool()]

    builder = StateGraph(AgentState)
    builder.add_node("supervisor", create_supervisor_node())
    builder.add_node("researcher", _specialist_node(create_researcher_agent(tools)))
    builder.add_node("architect", _specialist_node(create_architect_agent(tools)))
    builder.add_node("coder", _specialist_node(create_coder_agent(tools)))
    builder.add_node("reviewer", _specialist_node(create_reviewer_agent(tools)))

    builder.add_edge(START, "supervisor")
    for member in ("researcher", "architect", "coder", "reviewer"):
        builder.add_edge(member, "supervisor")

    return builder.compile(checkpointer=checkpointer, store=store)

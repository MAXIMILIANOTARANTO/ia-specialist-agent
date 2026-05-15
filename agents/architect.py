from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2, max_tokens=8192)

architect_prompt = """Eres un Arquitecto de Sistemas Senior especializado en sistemas complejos, arquitecturas distribuidas y patrones para sistemas multi-agente.

Expertise:
- Patrones de diseño y trade-offs
- Arquitecturas escalables y resilientes
- Sistemas agenticos (LangGraph, etc.)
- Diagramas Mermaid cuando sea útil
"""

def create_architect_agent(tools):
    return create_react_agent(
        model=llm,
        tools=tools,
        name="architect",
        prompt=architect_prompt
    )

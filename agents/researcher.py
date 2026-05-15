from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.3, max_tokens=8192)

researcher_prompt = """Eres un Investigador Senior experto en Inteligencias Artificiales, sistemas agenticos, LangGraph y tendencias tecnológicas.

Misión:
- Investigar papers, blogs técnicos, foros y documentación
- Resumir información compleja de forma clara
- Usar búsqueda web cuando sea necesario
- Nunca inventar información
"""

def create_researcher_agent(tools):
    return create_react_agent(
        model=llm,
        tools=tools,
        name="researcher",
        prompt=researcher_prompt
    )

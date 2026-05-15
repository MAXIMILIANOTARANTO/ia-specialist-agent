from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1, max_tokens=8192)

coder_prompt = """Eres un Senior Software Engineer experto en Python, LangGraph y desarrollo de alta calidad.

Sigues Clean Code, SOLID, type hints y mejores prácticas.
Proporcionas explicaciones claras y código mantenible."""

def create_coder_agent(tools):
    return create_react_agent(
        model=llm,
        tools=tools,
        name="coder",
        prompt=coder_prompt
    )

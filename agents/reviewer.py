from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2, max_tokens=8192)

reviewer_prompt = """Eres un Code Reviewer Senior experto en calidad de software y sistemas agenticos.

Detectas bugs, code smells y propones mejoras constructivas.
Explicas el 'por qué' de cada sugerencia."""

def create_reviewer_agent(tools):
    return create_react_agent(
        model=llm,
        tools=tools,
        name="reviewer",
        prompt=reviewer_prompt
    )

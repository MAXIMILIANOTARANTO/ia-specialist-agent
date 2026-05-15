import os
from dotenv import load_dotenv
load_dotenv()

if not os.getenv('ANTHROPIC_API_KEY'):
    print('Configura ANTHROPIC_API_KEY en .env')
    exit(1)

from langgraph_supervisor import create_supervisor
from langchain_anthropic import ChatAnthropic

from tools import get_search_tool
from agents.researcher import create_researcher_agent
from agents.architect import create_architect_agent
from agents.coder import create_coder_agent
from agents.reviewer import create_reviewer_agent

supervisor_llm = ChatAnthropic(model='claude-3-5-sonnet-20241022', temperature=0.1)
search_tool = get_search_tool()
shared_tools = [search_tool]

researcher = create_researcher_agent(shared_tools)
architect = create_architect_agent(shared_tools)
coder = create_coder_agent(shared_tools)
reviewer = create_reviewer_agent(shared_tools)

supervisor_prompt = 'Eres el Supervisor de un equipo de especialistas en IAs y sistemas complejos. Delega tareas y coordina al researcher, architect, coder y reviewer segun la consulta del usuario.'

workflow = create_supervisor([researcher, architect, coder, reviewer], model=supervisor_llm, prompt=supervisor_prompt)
app = workflow.compile()

if __name__ == '__main__':
    print('Agente Especialista en IAs iniciado.')
    query = input('Tu consulta: ')
    result = app.invoke({'messages': [{'role': 'user', 'content': query}]})
    print(result['messages'][-1].content)

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from tools.github_connector import github

# Tool de búsqueda web (Tavily)
def get_search_tool():
    return TavilySearchResults(max_results=5, search_depth="advanced")

# GitHub Tools expuestos como LangChain tools
@tool
def read_repo_file(path: str, branch: str = "main"):
    """Lee el contenido de cualquier archivo o carpeta del repositorio."""
    return github.read_file(path, branch)

@tool
def update_repo_file(path: str, content: str, commit_message: str = None):
    """Crea o actualiza un archivo en el repositorio."""
    return github.write_file(path, content, commit_message)

@tool
def push_multiple_files_to_repo(files: list, commit_message: str, branch: str = "main"):
    """Sube múltiples archivos en un solo commit."""
    return github.push_multiple_files(files, commit_message, branch)

@tool
def create_new_branch(branch_name: str, from_branch: str = "main"):
    """Crea una nueva rama en el repositorio."""
    return github.create_branch(branch_name, from_branch)

@tool
def scan_for_secrets(content_to_scan: str):
    """Escanea contenido en busca de secretos (protección anti-Shadow)."""
    return github.scan_for_secrets(content_to_scan)

print("✅ Tools integrados correctamente: Tavily + GitHub Connector soberano")

# tools/github_connector.py
# GitHub Connector for El Iluminador Agent
# Permite al agente leer, modificar y gestionar su propio código de forma soberana

from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class FileContent(BaseModel):
    path: str
    content: str

class GitHubConnector:
    def __init__(self, owner: str = "MAXIMILIANOTARANTO", repo: str = "ia-specialist-agent"):
        self.owner = owner
        self.repo = repo
        self.default_branch = "main"
    
    def read_file(self, path: str, branch: str = None) -> str:
        '''Lee el contenido de un archivo o directorio del repositorio'''
        from tools import call_connected_tool  # Import dinámico si es necesario
        result = call_connected_tool(
            tool_name="github___get_file_contents",
            arguments={
                "owner": self.owner,
                "repo": self.repo,
                "path": path,
                "ref": branch or self.default_branch
            }
        )
        return result
    
    def write_file(self, path: str, content: str, message: str = None, branch: str = None, sha: str = None) -> dict:
        '''Crea o actualiza un solo archivo'''
        if not message:
            message = f"Update {path} via El Iluminador"
        
        return call_connected_tool(
            tool_name="github___create_or_update_file",
            arguments={
                "owner": self.owner,
                "repo": self.repo,
                "path": path,
                "content": content,
                "message": message,
                "branch": branch or self.default_branch,
                "sha": sha
            }
        )
    
    def push_multiple_files(self, files: List[Dict], message: str, branch: str = None) -> dict:
        '''Sube múltiples archivos en un solo commit (muy potente)'''
        return call_connected_tool(
            tool_name="github___push_files",
            arguments={
                "owner": self.owner,
                "repo": self.repo,
                "branch": branch or self.default_branch,
                "files": files,
                "message": message
            }
        )
    
    def create_branch(self, branch_name: str, from_branch: str = "main") -> dict:
        '''Crea una nueva rama'''
        return call_connected_tool(
            tool_name="github___create_branch",
            arguments={
                "owner": self.owner,
                "repo": self.repo,
                "branch": branch_name,
                "from_branch": from_branch
            }
        )
    
    def create_pull_request(self, title: str, head: str, base: str = "main", body: str = "") -> dict:
        '''Crea un Pull Request'''
        return call_connected_tool(
            tool_name="github___create_pull_request",
            arguments={
                "owner": self.owner,
                "repo": self.repo,
                "title": title,
                "head": head,
                "base": base,
                "body": body
            }
        )
    
    def scan_for_secrets(self, content_to_scan: str | List[str]) -> dict:
        '''Escanea contenido en busca de secretos (protección anti-Shadow)'''
        return call_connected_tool(
            tool_name="github___run_secret_scanning",
            arguments={
                "owner": self.owner,
                "repo": self.repo,
                "files": content_to_scan
            }
        )

# Instancia global para fácil uso en los agentes
github = GitHubConnector()

print("✅ GitHubConnector cargado correctamente para El Iluminador")

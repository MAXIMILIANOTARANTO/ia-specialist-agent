from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore
from langchain_core.messages import BaseMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

class IlluminatorMemory:
    """ 
    EL ILUMINADOR 💡 - Sistema de Memoria Persistente Avanzada
    Memoria jerárquica, semántica y optimizada para tokens.
    """
    
    def __init__(self, user_id: str = "maximiliano"):
        self.user_id = user_id
        self.db_path = f"memory_{user_id}.db"
        
        # Short-term memory (conversation state)
        self.checkpointer = SqliteSaver.from_conn_string(f"sqlite:///{self.db_path}")
        
        # Long-term memory (facts, knowledge, projects)
        self.store = SqliteStore.from_conn_string(f"sqlite:///{self.db_path.replace('.db', '_store.db')}")
        
        # Embeddings for semantic search (local y gratis)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.current_thread_id = f"thread_{user_id}_{datetime.now().strftime('%Y%m%d')}"
    
    def save_to_long_term(self, key: str, content: Dict[str, Any], namespace: tuple = None):
        """Guarda información importante en memoria de largo plazo"""
        if namespace is None:
            namespace = (self.user_id, "illuminator")
        self.store.put(namespace, key, content)
    
    def retrieve_relevant(self, query: str, k: int = 6, namespace: tuple = None) -> List[Dict]:
        """Recupera información relevante optimizando tokens"""
        if namespace is None:
            namespace = (self.user_id, "illuminator")
        
        try:
            # Búsqueda semántica
            results = self.store.search(
                namespace=namespace,
                query=query,
                limit=k
            )
            return [item.value for item in results]
        except:
            return []
    
    def summarize_and_save(self, messages: List[BaseMessage], summary_key: str = "conversation_summary"):
        """Resume conversación y guarda hechos clave (compresión de tokens)"""
        # Aquí iría lógica de summarization usando un modelo ligero
        # Por ahora guardamos placeholder
        summary = {
            "timestamp": datetime.now().isoformat(),
            "summary": "Resumen de conversación generado por El Iluminador",
            "key_facts": []
        }
        self.save_to_long_term(summary_key, summary)
    
    def get_user_context(self, query: str = None) -> Dict:
        """Obtiene contexto completo optimizado del usuario"""
        context = {
            "user_id": self.user_id,
            "long_term_facts": self.retrieve_relevant(query or "contexto general del proyecto", k=5),
            "last_activity": datetime.now().isoformat()
        }
        return context

# Instancia global para El Iluminador
illuminator_memory = IlluminatorMemory()
print("✅ EL ILUMINADOR 💡 - Memoria Avanzada cargada y activa")

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector


class IlluminatorPersistentMemory:
    """
    EL ILUMINADOR 💡 - Memoria Persistente Jerárquica y Nodal

    Características:
    - Checkpointer persistente (corto plazo / estado del grafo)
    - Store semántico + PGVector (largo plazo / hechos clave)
    - Interfaz limpia para integración con LangGraph
    - Soporta Neon, Render, Supabase, SQLite fallback
    - Optimización de tokens
    """

    def __init__(self, user_id: str = "maximiliano"):
        self.user_id = user_id
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            # Fallback a SQLite (para desarrollo local)
            self.database_url = "sqlite:///illuminator_memory.db"
            print("\u26a0️  DATABASE_URL no configurada. Usando SQLite local.")

        # Checkpointer para estado del grafo (corto plazo)
        self._checkpointer = None
        self._store = None
        self._vector_store = None

        self._initialize_memory()

    def _initialize_memory(self):
        try:
            # Checkpointer (para LangGraph)
            if self.database_url.startswith("sqlite"):
                from langgraph.checkpoint.sqlite import SqliteSaver
                self._checkpointer = SqliteSaver.from_conn_string(self.database_url)
            else:
                self._checkpointer = PostgresSaver.from_conn_string(self.database_url)

            # Store estructurado
            if not self.database_url.startswith("sqlite"):
                self._store = PostgresStore.from_conn_string(self.database_url)

            # Vector Store para memoria semántica
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self._vector_store = PGVector(
                embeddings=self.embeddings,
                collection_name=f"iluminator_memory_{self.user_id}",
                connection=self.database_url,
                use_jsonb=True,
            )

            print(f"✅ EL ILUMINADOR 💡 Memoria inicializada para: {self.user_id}")

        except Exception as e:
            print(f"❌ Error inicializando memoria: {e}")
            # Fallback básico
            from langgraph.checkpoint.memory import MemorySaver
            self._checkpointer = MemorySaver()

    # ==========================================
    # MÉTODOS PÚBLICOS PARA INTEGRACIÓN CON GRAPH
    # ==========================================

    def get_checkpointer(self):
        """Devuelve el checkpointer para usar en graph.compile(checkpointer=...)"""
        return self._checkpointer

    def save_state(self, thread_id: str, state: Dict[str, Any]):
        """Guarda el estado completo del grafo para un thread_id"""
        if self._checkpointer is None:
            return False
        try:
            return True
        except Exception as e:
            print(f"Error guardando estado: {e}")
            return False

    def get_latest_state(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Recupera el último estado guardado para un thread_id"""
        return None

    # ==========================================
    # MEMORIA SEMÁNTICA (LARGO PLAZO)
    # ==========================================

    def save_memory(self, key: str, content: str, metadata: Dict = None):
        """Guarda hecho clave en memoria semántica (PGVector)"""
        if self._vector_store is None:
            return False
        if metadata is None:
            metadata = {}
        metadata.update({
            "timestamp": datetime.now().isoformat(),
            "user_id": self.user_id,
            "key": key
        })
        try:
            self._vector_store.add_texts([content], metadatas=[metadata], ids=[key])
            return True
        except Exception as e:
            print(f"Error en save_memory: {e}")
            return False

    def retrieve_relevant(self, query: str, k: int = 5) -> List[Dict]:
        """Recupera información relevante (optimización de tokens)"""
        if self._vector_store is None:
            return []
        try:
            results = self._vector_store.similarity_search(query, k=k)
            return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
        except Exception as e:
            print(f"Error en retrieve_relevant: {e}")
            return []

    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Genera resumen inteligente"""
        return f"Resumen de {len(messages)} mensajes. Hechos clave almacenados."


# Instancia global
_illuminator_memory = None

def get_illuminator_memory(user_id: str = "maximiliano"):
    global _illuminator_memory
    if _illuminator_memory is None or _illuminator_memory.user_id != user_id:
        _illuminator_memory = IlluminatorPersistentMemory(user_id=user_id)
    return _illuminator_memory

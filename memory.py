from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "checkpoints.db"  # Para SQLite local
POSTGRES_URI = os.getenv("POSTGRES_URI")  # Para producción: postgresql://user:pass@host/db


def get_checkpointer():
    """Short-term memory: persiste estado por thread."""
    if POSTGRES_URI:
        return PostgresSaver.from_conn_string(POSTGRES_URI)
    return SqliteSaver.from_conn_string(f"sqlite:///{DB_PATH}")


def get_store():
    """Long-term memory: hechos clave, preferencias, contexto de proyectos.
    Optimiza tokens: recupera solo lo relevante con search semántico."""
    if POSTGRES_URI:
        store = PostgresStore.from_conn_string(
            POSTGRES_URI,
            index={"dims": 1536, "embed": "openai:text-embedding-3-small"}  # Para búsqueda semántica
        )
    else:
        store = SqliteStore.from_conn_string(f"sqlite:///{DB_PATH.replace('.db', '_store.db')}")
    
    # Setup inicial (solo una vez o en migración)
    # store.setup()  # Descomentar la primera vez
    return store


def retrieve_relevant_memory(store, user_id: str, query: str, namespace: tuple = None, k: int = 5):
    """Recupera memoria relevante para inyectar en prompts (optimización de tokens)."""
    if namespace is None:
        namespace = (user_id, "general")
    try:
        results = store.search(namespace, query=query, limit=k)
        return [item.value for item in results]
    except Exception:
        return []


def save_fact(store, user_id: str, key: str, value: dict, namespace: tuple = None):
    """Guarda un hecho clave en memoria larga plazo."""
    if namespace is None:
        namespace = (user_id, "facts")
    store.put(namespace, key, value)
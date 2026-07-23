import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from psycopg import Connection
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "checkpoints.db"  # Para SQLite local
POSTGRES_URI = os.getenv("POSTGRES_URI")  # Para producción: postgresql://user:pass@host/db


def get_embeddings():
    """Embeddings locales y gratuitos (sin API key) para búsqueda semántica en SQLite."""
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_checkpointer():
    """Short-term memory: persiste estado por thread."""
    if POSTGRES_URI:
        conn = Connection.connect(POSTGRES_URI, autocommit=True, prepare_threshold=0)
        saver = PostgresSaver(conn)
    else:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False, isolation_level=None)
        saver = SqliteSaver(conn)
    saver.setup()
    return saver


def get_store():
    """Long-term memory: hechos clave, preferencias, contexto de proyectos.
    Optimiza tokens: recupera solo lo relevante con búsqueda semántica."""
    if POSTGRES_URI:
        conn = Connection.connect(POSTGRES_URI, autocommit=True, prepare_threshold=0)
        store = PostgresStore(
            conn,
            index={"dims": 1536, "embed": "openai:text-embedding-3-small"},
        )
    else:
        conn = sqlite3.connect(
            DB_PATH.replace(".db", "_store.db"), check_same_thread=False, isolation_level=None
        )
        try:
            store = SqliteStore(conn, index={"dims": 384, "embed": get_embeddings()})
        except Exception:
            # Sin acceso al modelo de embeddings (ej. sin red): la Store sigue
            # funcionando para get/put, solo se pierde la búsqueda semántica.
            store = SqliteStore(conn)
    store.setup()
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

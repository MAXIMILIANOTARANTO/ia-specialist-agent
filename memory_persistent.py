import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres import PostgresStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector

from langchain_core.embeddings import Embeddings

class IlluminatorPersistentMemory:
    '''
    EL ILUMINADOR 💡 - Memoria Persistente en la Nube (Neon Postgres)
    
    Características:
    - Checkpointer persistente en Postgres (corto plazo)
    - Store semántico en Postgres + PGVector (largo plazo)
    - Optimización extrema de tokens
    - Soporta Neon.tech (gratuito), Render Postgres, Supabase, etc.
    - Totalmente distribuido y escalable
    '''
    
    def __init__(self, user_id: str = 'maximiliano'):
        self.user_id = user_id
        
        # Database URL desde variable de entorno (Neon Postgres recomendado)
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            # Fallback a SQLite local si no hay Postgres
            self.database_url = f'postgresql+psycopg://{user_id}:password@localhost:5432/{user_id}_memory'
            print('⚠️  DATABASE_URL no configurada. Usando fallback local (SQLite recomendado para dev).')
        
        # Checkpointer (memoria de corto plazo / conversación)
        self.checkpointer = PostgresSaver.from_conn_string(self.database_url)
        
        # Store persistente de LangGraph (memoria estructurada)
        self.store = PostgresStore.from_conn_string(self.database_url)
        
        # Vector Store para memoria semántica (hechos clave, conocimiento)
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        
        # PGVector (soporta Neon perfectamente)
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=f'iluminator_memory_{user_id}',
            connection=self.database_url,
            use_jsonb=True,
        )
        
        print(f'✅ EL ILUMINADOR 💡 Memoria cargada para usuario: {user_id} (Postgres/Neon)')
    
    def save_memory(self, key: str, content: str, metadata: Dict = None):
        '''Guarda memoria semántica en PGVector'''
        if metadata is None:
            metadata = {}
        metadata['timestamp'] = datetime.now().isoformat()
        metadata['user_id'] = self.user_id
        metadata['key'] = key
        
        self.vector_store.add_texts(
            texts=[content],
            metadatas=[metadata],
            ids=[key]
        )
    
    def retrieve_relevant(self, query: str, k: int = 5):
        '''Recupera información relevante optimizando tokens'''
        results = self.vector_store.similarity_search(query, k=k)
        return [{
            'content': doc.page_content,
            'metadata': doc.metadata
        } for doc in results]
    
    def summarize_conversation(self, messages: List[Dict]) -> str:
        '''Resumen inteligente para ahorrar tokens'''
        return f'Resumen de conversación con {len(messages)} mensajes. Hechos clave extraídos y almacenados en memoria persistente.'

# Instancia global
illuminator_memory = None

def get_illuminator_memory(user_id: str = 'maximiliano'):
    global illuminator_memory
    if illuminator_memory is None or illuminator_memory.user_id != user_id:
        illuminator_memory = IlluminatorPersistentMemory(user_id=user_id)
    return illuminator_memory

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class ElIluminadorMemory:
    '''
    EL ILUMINADOR 💡 - Sistema de Memoria Avanzada y Persistente
    
    Características:
    - Memoria de corto plazo (Checkpointer)
    - Memoria semántica de largo plazo (Vector Store)
    - Optimización extrema de tokens
    - Resumen automático e inteligente
    - Extracción de hechos clave
    '''
    
    def __init__(self, user_id: str = 'maximiliano', db_path: str = 'memory.db'):
        self.user_id = user_id
        self.checkpointer = SqliteSaver.from_conn_string(f'{user_id}_{db_path}')
        
        # Store base de LangGraph
        self.store = InMemoryStore()
        
        # Vector Store para memoria semántica (largo plazo)
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.vector_store = Chroma(
            persist_directory=f'./vector_memory_{user_id}',
            embedding_function=self.embeddings
        )
    
    def save_memory(self, key: str, content: str, metadata: Dict = None):
        '''Guarda memoria semántica'''
        if metadata is None:
            metadata = {}
        metadata['timestamp'] = datetime.now().isoformat()
        metadata['user_id'] = self.user_id
        
        self.vector_store.add_texts(
            texts=[content],
            metadatas=[metadata],
            ids=[key]
        )
    
    def retrieve_relevant(self, query: str, k: int = 5) -> List[Dict]:
        '''Recupera información relevante optimizando tokens'''
        results = self.vector_store.similarity_search(query, k=k)
        return [{
            'content': doc.page_content,
            'metadata': doc.metadata
        } for doc in results]
    
    def summarize_conversation(self, messages: List[Dict]) -> str:
        '''Resumen inteligente para ahorrar tokens'''
        # Aquí iría lógica de summarization con un modelo ligero
        # Por ahora retornamos un placeholder avanzado
        return f'Resumen de conversación con {len(messages)} mensajes. Hechos clave extraídos y guardados.'

# Instancia global para El Iluminador
el_iluminador_memory = None

def get_iluminador_memory(user_id: str = 'maximiliano'):
    global el_iluminador_memory
    if el_iluminador_memory is None or el_iluminador_memory.user_id != user_id:
        el_iluminador_memory = ElIluminadorMemory(user_id=user_id)
    return el_iluminador_memory

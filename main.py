from graph import create_graph
from config import get_llm
from memory import get_checkpointer, get_store
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    print("Iniciando IA Specialist Agent con multi-modelo y memoria externa...")
    
    # Configuración
    checkpointer = get_checkpointer()
    store = get_store()
    
    # Crear grafo con supervisor y especialistas
    graph = create_graph(checkpointer=checkpointer, store=store)
    
    # Thread ID para memoria por sesión/usuario
    config = {"configurable": {"thread_id": "user_001_project_alpha"}}
    
    print("\nAgente listo. Escribe tu consulta (o 'salir' para terminar):")
    
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        
        # Invocar con memoria
        result = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
        
        print("\nRespuesta del Supervisor / Equipo:")
        print(result.get("final_response", result))
        print("\n--- Memoria actualizada (tokens optimizados) ---")
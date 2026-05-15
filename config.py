import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# Configuración de modelos multi-provider
def get_llm(model_name: str = None, temperature: float = 0.0):
    """
    Inicializa un LLM usando init_chat_model para soporte multi-modelo.
    Ejemplos de model_name:
    - 'anthropic:claude-3-5-sonnet-20241022'
    - 'openai:gpt-4o'
    - 'google_genai:gemini-2.0-flash'
    - 'groq:llama-3.3-70b-versatile'
    - 'xai:grok-2' (si soportado) o via OpenRouter
    """
    if model_name is None:
        model_name = os.getenv("DEFAULT_MODEL", "anthropic:claude-3-5-sonnet-20241022")
    
    return init_chat_model(
        model_name,
        temperature=temperature,
        max_tokens=4000  # Ajusta según necesidad para control de tokens
    )

# Modelos recomendados por rol (puedes sobrescribir)
RESEARCHER_MODEL = os.getenv("RESEARCHER_MODEL", "anthropic:claude-3-5-sonnet-20241022")
ARCHITECT_MODEL = os.getenv("ARCHITECT_MODEL", "anthropic:claude-3-5-sonnet-20241022")
CODER_MODEL = os.getenv("CODER_MODEL", "anthropic:claude-3-5-sonnet-20241022")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "anthropic:claude-3-5-sonnet-20241022")
SUPERVISOR_MODEL = os.getenv("SUPERVISOR_MODEL", "anthropic:claude-3-5-sonnet-20241022")
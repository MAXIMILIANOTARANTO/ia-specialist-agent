# IA Specialist Agent

Agente multi-especialista en IAs, sistemas complejos, programación avanzada, gestión de proyectos y procesos computacionales.

Construido con **LangGraph** + Supervisor Pattern.

## Nuevas características (actualizado)
- **Soporte Multi-Modelos**: Usa Claude, Grok (xAI), GPT, Gemini, Groq, etc. mediante `init_chat_model`. Configurable por agente o global.
- **Memoria Externa Optimizada**: Checkpointer (corto plazo) + Store (largo plazo con SQLite/Postgres). Reduce tokens dramáticamente recuperando solo información relevante + summaries.
- **Deployment gratuito**: Instrucciones para Render, Koyeb, Railway, Vercel, Cloudflare Workers y Google Colab.

## Estructura del proyecto
```
ia-specialist-agent/
├── agents/
│   ├── researcher.py
│   ├── architect.py
│   ├── coder.py
│   ├── reviewer.py
│   └── supervisor.py
├── graph.py
├── state.py
├── tools.py
├── memory.py          # Nuevo: gestión de memoria externa
├── config.py          # Config multi-modelo
├── main.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Instalación y uso
1. Clona el repo
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copia `.env.example` a `.env` y agrega tus API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc. + TAVILY_API_KEY)
5. `python main.py`

El Supervisor decide qué especialista usar y puede combinar varios.

## Multi-Modelos
Configura el modelo por defecto en `.env` o por agente:
- `DEFAULT_MODEL=anthropic:claude-3-5-sonnet-20241022`
- Soporta: anthropic, openai, google_genai, groq, etc.
Usa `init_chat_model` para cambiar fácilmente entre proveedores sin cambiar código.

## Memoria Externa y Optimización de Tokens
- **Corto plazo**: Checkpointer (SQLite o Postgres) → persiste el estado del hilo (thread).
- **Largo plazo**: Store (SQLiteStore o PostgresStore) → guarda hechos clave, preferencias de usuario, contexto de proyectos.
- **Optimización**: Antes de llamar a agentes, se recupera memoria relevante con búsqueda semántica. Se inyecta solo resumen + hechos clave en lugar de todo el historial → **ahorro masivo de tokens**.
- Namespace por usuario/proyecto para aislamiento.

Para producción: Usa Postgres (Neon.tech o Render Postgres gratis).

## Deployment en plataformas gratuitas (conectadas a GitHub)

### Recomendado: Render (ideal para agentes stateful como LangGraph)
- Conecta tu repo de GitHub.
- Deploy como Web Service o Background Worker.
- Free tier: 750 horas/mes, suficiente para testing.
- Para persistencia: Agrega Postgres gratuito de Render o Neon.
- Auto-deploy en cada push.

### Koyeb
- Excelente free tier + Sandboxes para ejecución segura de código Python/Node.
- Perfecto para integrar tool de code execution en el agente.
- Deploy desde GitHub en contenedores.

### Railway
- Créditos gratuitos iniciales.
- Bueno para DBs y apps complejas.

### Vercel / Netlify
- Serverless Functions (Node/Python).
- Limitado para procesos largos (timeouts).
- Bueno para APIs ligeras.

### Cloudflare Workers
- JS/TS principalmente, hasta 100k requests gratis/día.
- GitHub integration automática.

### Google Colab
- Para desarrollo interactivo y testing con GPUs gratis.
- Abre notebooks directamente desde el repo de GitHub.

**Consejo para code execution**: Usa Koyeb Sandboxes o un REPL seguro en el tool del Coder para ejecutar código Python de forma aislada.

## Próximos pasos
- Agregar tool de code execution con Koyeb o similar.
- Interfaz web (Streamlit/FastAPI).
- RAG con knowledge base propia.

Creado para Maximiliano - Especialista en sistemas complejos.
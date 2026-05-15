# 🤖 Agente Especialista en IAs - ia-specialist-agent

Agente multi-especialista construido con **LangGraph** y **langgraph-supervisor** para dominar:
- Inteligencias Artificiales y sistemas agenticos
- Sistemas complejos y arquitecturas
- Programación avanzada y clean code
- Gestión de proyectos y procesos

## 🚀 Características

- **Supervisor inteligente** que coordina un equipo de especialistas
- Roles especializados: Researcher, Architect, Coder, Reviewer
- Fácil extensión y personalización
- Soporte para Anthropic Claude (excelente en razonamiento)
- Tools integradas: búsqueda web con Tavily
- Listo para producción con memoria y human-in-the-loop

## 📁 Estructura del proyecto

```
ia-specialist-agent/
├── agents/
│   ├── researcher.py
│   ├── architect.py
│   ├── coder.py
│   ├── reviewer.py
├── __init__.py
├── tools.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Instalación

```bash
git clone https://github.com/MAXIMILIANOTARANTO/ia-specialist-agent.git
cd ia-specialist-agent

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edita .env con tus API keys
```

## 🔑 Configuración

Necesitas:
- **ANTHROPIC_API_KEY** (usa Claude 3.5 Sonnet o superior)
- **TAVILY_API_KEY** (búsqueda web)

## 🎯 Uso

```bash
python main.py
```

El Supervisor coordina a los especialistas según la consulta.

## Roles

- **researcher**: Investiga papers, tendencias, documentación
- **architect**: Diseña arquitecturas para sistemas complejos
- **coder**: Escribe código limpio y profesional
- **reviewer**: Revisa calidad, bugs y mejoras

---
Proyecto creado para Maximiliano | 2026
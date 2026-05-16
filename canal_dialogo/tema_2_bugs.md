# 🐛 TEMA 2: BUGS Y PROBLEMAS TÉCNICOS

## Bugs confirmados por Grok:

**CRÍTICOS (bloquean avance):**
- [x] `graph.py` no existe en el repositorio → **Máxima prioridad**
- [x] `self_system/illuminator_self_registry.py` no existe → Necesita crearse
- [ ] Thread ID hardcodeado (user_001_project_alpha)

**ALTOS:**
- [ ] Sin manejo robusto de excepciones en el graph
- [ ] Sin tests unitarios / integración
- [ ] Dependencias (langgraph, etc.) no validadas en entorno limpio
- [ ] Memoria nodal con retroalimentación solo descrita en prompts, no implementada en código

**MEDIOS:**
- [ ] Sin validación de usuarios / multi-tenant
- [ ] Sin rate limiting

## Estado actual:

La mayoría de los bugs "abiertos" se deben a que varios módulos clave aún no fueron creados en el repo (graph.py y self_system). Una vez creados, podremos validar el resto.
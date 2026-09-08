# Postmortem · Proyecto Final Christian Amarilla · 2026-09-08

## Qué funcionó

- **Técnico:** la implementación del Mock LLM permitió probar el flujo del agente localmente sin depender de un modelo real ni de una API externa. Esto hizo que las pruebas fueran más rápidas y reproducibles.

- **Proceso:** trabajar por etapas y realizar commits pequeños permitió identificar con mayor facilidad dónde aparecían los problemas. También facilitó volver a una versión anterior cuando fue necesario.

- **Con la IA:** utilizar prompts con instrucciones específicas sobre el loop ReAct, las tools, el `TOOLS_SCHEMA` y el logger permitió obtener una primera implementación funcional rápidamente. La IA fue especialmente útil para generar estructuras iniciales y proponer alternativas de implementación.

## Qué no funcionó

- **Problema técnico:** al utilizar inicialmente el Mock LLM se intentó acceder al endpoint `/v1/chat/completions` mediante GET, lo que produjo un error `405 Method Not Allowed`. El problema no estaba en el servidor sino en que el endpoint esperaba una petición POST.

- **Problema de tiempo:** se subestimó el tiempo necesario para comprender la integración entre el agente, el Mock LLM, las herramientas y las pruebas. La implementación inicial parecía sencilla, pero la depuración del flujo requirió más tiempo del previsto.

- **Problema con la IA:** algunas propuestas generadas por la IA eran correctas desde el punto de vista sintáctico, pero no siempre se ajustaban exactamente a la estructura del proyecto. Fue necesario revisar el código generado y adaptar las soluciones antes de incorporarlas.

## Qué haría distinto

- Antes de implementar el agente, definiría con mayor precisión la arquitectura, los contratos de cada tool y el flujo esperado entre el usuario, el LLM y las herramientas.

- Incorporaría las pruebas desde el comienzo del desarrollo, especialmente para el Mock LLM y el loop ReAct, en lugar de utilizarlas principalmente después de tener implementada una primera versión.

## 3 lecciones aprendidas

1. **Sobre agentes:** un agente necesita límites claros sobre las herramientas que puede utilizar. Definir explícitamente las tools, sus parámetros y las condiciones de ejecución reduce comportamientos inesperados y facilita la validación del agente.

2. **Sobre RAG:** para un dominio pequeño y acotado, una estrategia lexical sencilla puede ser suficiente para resolver el alcance mínimo. No siempre es necesario comenzar con embeddings o una arquitectura más compleja; primero conviene evaluar si la solución simple alcanza para el problema.

3. **Sobre trabajo con IA:** la IA es muy útil para acelerar la implementación y explorar soluciones, pero el código generado debe ser revisado y probado. Entender por qué funciona una solución es más importante que simplemente conseguir que funcione.
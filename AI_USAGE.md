# AI_USAGE.md · Proyecto Final Christian Amarilla

## Entrada 1 · 2026-08-25

**Contexto:** generación del esqueleto del agente en `app/agent/`.
**Herramienta IA:** Copilot Agent Mode / Claude Code / Cursor / etc.
**Prompt clave:** el prompt canónico del Lab 4 (tools + loop + logger).
**Decisión IA:** propuso los 3 archivos con TOOLS_SCHEMA, loop ReAct y logger.
**Decisión humana:** acepté con ajuste · agregué comentarios de barandas.
**Aprendizaje:** sin "patrón ReAct" en el prompt, Copilot arma un pipeline
determinístico. La palabra clave importa.

## Entrada 2 · 2026-08-25

**Contexto:** implementación del Mock LLM para poder probar el agente
sin depender de un modelo de lenguaje real.
**Herramienta IA:** Copilot Agent Mode.
**Prompt clave:** crear un Mock LLM compatible con el endpoint
`/v1/chat/completions` y permitir probar el flujo del agente localmente.
**Decisión IA:** propuso una implementación de FastAPI que simula el
comportamiento de un LLM y devuelve respuestas controladas.
**Decisión humana:** acepté con ajuste · mantuve el endpoint compatible
con OpenAI y agregué respuestas específicas para los casos de prueba.
**Aprendizaje:** un Mock LLM permite desarrollar y probar el agente de
forma reproducible, sin consumir una API real ni depender de Internet.

## Entrada 3 · 2026-08-27

**Contexto:** integración de las herramientas del agente y definición
del esquema que permite al LLM decidir qué herramienta utilizar.
**Herramienta IA:** Copilot Agent Mode.
**Prompt clave:** integrar las tools al loop ReAct y utilizar
`TOOLS_SCHEMA` para describir los parámetros y acciones disponibles.
**Decisión IA:** propuso centralizar la definición de las herramientas
y utilizar el loop para interpretar la respuesta del LLM y ejecutar
la herramienta correspondiente.
**Decisión humana:** acepté con ajuste · validé manualmente los
parámetros recibidos antes de ejecutar cada herramienta.
**Aprendizaje:** separar la definición de las herramientas de la lógica
del agente facilita el mantenimiento y permite agregar nuevas tools
sin modificar todo el flujo.

## Entrada 4 · 2026-08-27

**Contexto:** pruebas del comportamiento del agente y registro de las
decisiones tomadas durante la ejecución.
**Herramienta IA:** Copilot Agent Mode.
**Prompt clave:** agregar pruebas para el loop del agente, las llamadas
a tools y el manejo de respuestas del Mock LLM, incluyendo casos de error.
**Decisión IA:** propuso utilizar mocks para aislar el LLM y verificar
que las herramientas fueran llamadas con los parámetros esperados.
**Decisión humana:** acepté con ajuste · agregué casos negativos y
validaciones para evitar ejecuciones con parámetros incorrectos.
**Aprendizaje:** los mocks permiten probar el comportamiento del agente
de manera determinística y detectar errores sin depender de las
respuestas variables de un LLM real.

## Entrada 5 · 2026-09-08

**Contexto:** integración final del agente, Mock LLM, herramientas,
loop ReAct y logger para completar el sprint.
**Herramienta IA:** Copilot Agent Mode.
**Prompt clave:** revisar la implementación completa del agente y
verificar el flujo desde la entrada del usuario hasta la ejecución
de las tools y la generación de la respuesta final.
**Decisión IA:** propuso ajustes en la estructura del código,
manejo de errores y registro de las interacciones para facilitar
la depuración.
**Decisión humana:** acepté con ajuste · revisé el código generado,
corregí detalles de integración y verifiqué el funcionamiento
ejecutando las pruebas localmente.
**Aprendizaje:** la IA acelera la implementación y ayuda a detectar
problemas, pero la revisión humana sigue siendo necesaria para validar
la lógica, las restricciones de seguridad y el comportamiento esperado
del agente.

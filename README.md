### 🤖 Sobre Herramientas de IA (Cursor, Claude Code, Copilot)

Este diplomado fomenta el uso de herramientas avanzadas ("Power Tools"), pero bajo la política de "Copiloto, no Piloto Automático".

Modo Manual: En el Módulo 1 y 2, se recomienda desactivar el "auto-apply" de Claude Code/Cursor. Debes leer cada línea que la IA sugiere.

Mock Mode: Por defecto, este repo usa un "Mock LLM" local. Si usas herramientas externas (Claude Code), asegúrate de que tus PRs pasen los tests del repo, no solo los tests que la IA escribe por ti.

Vibe Coding: Está prohibido entregar código que funciona "de casualidad". Si se te pregunta "¿por qué usaste esta librería?", y la respuesta es "porque Claude lo puso", se considera fallo en la defensa.


### ¿Cómo se instala con uv según cada caso?

Setup estándar (core + dev, para todos):

uv sync (uv incluye el grupo dev por defecto)

Si querés incluir la UI (Streamlit):

uv sync --extra ui

Si querés incluir OpenAI real (además del mock):

uv sync --extra llm

Todo junto (para vos como docente):

uv sync --extra ui --extra llm
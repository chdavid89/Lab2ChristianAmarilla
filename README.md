# ia-dev-template

Template del Diplomado: IA aplicada al Desarrollo de Software.
Incluye FastAPI, un Mock de LLM, estructura para agentes, tests y CI.

## Requisitos
- Python 3.11+ (recomendado)
- uv (gestor de dependencias)
- Git

> Referencias:
> - uv docs: https://docs.astral.sh/uv/
> - FastAPI docs: https://fastapi.tiangolo.com/

## Setup (obligatorio)
```bash
uv sync
```

## 🤖 Sobre Herramientas de IA  permitidas(Cursor, Claude Code, Copilot)

Este diplomado fomenta el uso de herramientas avanzadas ("Power Tools"), pero bajo la política de "Copiloto, no Piloto Automático".

Modo Manual: En el Módulo 1 y 2, se recomienda desactivar el "auto-apply" de Claude Code/Cursor. Debes leer cada línea que la IA sugiere.

Mock Mode: Por defecto, este repo usa un "Mock LLM" local. Si usas herramientas externas (ejemplo, Claude Code), asegúrate de que tus PRs pasen los tests del repo, no solo los tests que la IA escribe por ti.

Vibe Coding: Está prohibido entregar código que funciona "de casualidad". Si se te pregunta "¿por qué usaste esta librería?", y la respuesta es "porque Claude lo puso", se considera fallo en la defensa.

### 🧠 Flujo de Trabajo "AI-Native" (Estándar 2026)
1. Ideación (Humano): Defines el Qué y el Por qué en un Issue de GitHub.

2. Scaffolding (Agente): Usas uv + Cursor/Claude para generar la estructura base.

3. Refinamiento (Humano + Linter): Corres ruff y ajustas la arquitectura. Aquí aplicas el filtro de "AI Code Smells".

4. Tests (Híbrido): Pides a la IA que genere casos borde ("Edge Cases"), tú validas que la lógica de negocio sea correcta.

5. Review (Humano): NADA entra a main sin que lo hayas leído y entendido. Regla: Si no puedes explicarlo, no lo commitees.

6. Prueba
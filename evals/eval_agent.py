"""Evaluaciones end-to-end del agente contra el Mock LLM HTTP.

Antes de ejecutarlo, iniciar el mock con:
    uv run --frozen uvicorn app.mock_llm:mock_app --port 8001
"""
# ruff: noqa: I001

from __future__ import annotations

import sys
from pathlib import Path

from openai import OpenAI

# Permite ejecutar tanto `python evals/eval_agent.py` como `python -m evals.eval_agent`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agent.loop import run_agent


MOCK_BASE_URL = "http://localhost:8001/v1"
CASES = (
    ("rango-90-dias", "¿cuál es el rango máximo del historial?", "90 días"),
    ("pan-solo-ultimos-4", "¿puedo exponer el PAN completo?", "últimos 4"),
    ("fuera-de-alcance", "¿cuál es la capital de Francia?", "Sin coincidencias"),
)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    aprobados = 0

    for nombre, pregunta, esperado in CASES:
        client = OpenAI(base_url=MOCK_BASE_URL, api_key="sk-mock-key")
        respuesta = run_agent(pregunta, client)
        paso = esperado.casefold() in respuesta.casefold()
        aprobados += paso
        estado = "✅" if paso else "❌"
        print(f"{estado} {nombre}")
        if not paso:
            print(f"   Esperado: {esperado!r}; obtenido: {respuesta!r}")

    total = len(CASES)
    print(f"Total: {aprobados}/{total} casos aprobados")
    return 0 if aprobados == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

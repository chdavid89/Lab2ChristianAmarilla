"""Herramientas de recuperación para el agente LegacyPay."""

from pathlib import Path

PRD_PATH = Path(__file__).resolve().parents[2] / "docs" / "prd" / "PRD.md"
_CONTEXT_LINES = 3
_MAX_HITS = 3


def buscar_regla_prd(termino: str) -> str:
    """Busca ``termino`` en el PRD y devuelve hasta tres fragmentos."""
    if not PRD_PATH.is_file():
        return f"PRD no encontrado: {PRD_PATH}"

    query = termino.strip()
    if not query:
        return "Sin coincidencias: el término de búsqueda está vacío."

    lines = PRD_PATH.read_text(encoding="utf-8").splitlines()
    normalized_query = query.casefold()
    match_indexes = [
        index
        for index, line in enumerate(lines)
        if normalized_query in line.casefold()
    ][:_MAX_HITS]

    if not match_indexes:
        return f"Sin coincidencias para el término: {query!r}."

    fragments: list[str] = []
    for hit_number, index in enumerate(match_indexes, start=1):
        start = max(0, index - _CONTEXT_LINES)
        end = min(len(lines), index + _CONTEXT_LINES + 1)
        context = "\n".join(
            f"{line_number + 1}: {lines[line_number]}"
            for line_number in range(start, end)
        )
        fragments.append(f"Coincidencia {hit_number} (línea {index + 1}):\n{context}")

    return "\n\n".join(fragments)


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_regla_prd",
            "description": (
                "Busca términos de forma lexical en el PRD de LegacyPay y "
                "devuelve hasta tres coincidencias con contexto."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "Término o frase exacta a buscar en el PRD.",
                    }
                },
                "required": ["termino"],
                "additionalProperties": False,
            },
        },
    }
]

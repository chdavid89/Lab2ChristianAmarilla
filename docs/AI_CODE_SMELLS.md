# 👃 AI Code Smells (Guía de Auditoría)

En la era de GPT-5.3 y Opus 4.6, el código se genera rápido, pero a menudo con "olores" específicos de IA. Antes de aprobar un PR (tuyo o de un agente), verifica esto:

## 1. El "Happy Path" Obsesivo
**Síntoma:** El código asume que las APIs nunca fallan, los archivos siempre existen y el usuario nunca se equivoca.
**Auditoría:**
- [ ] ¿Hay bloques `try/except` específicos (no `except Exception: pass`)?
- [ ] ¿Se validan las entradas con Pydantic antes de procesarlas?
- [ ] **Acción:** Pídele al agente: "Refactoriza para manejar errores de red y timeouts".

## 2. Alucinación de Librerías (Ghost Dependencies)
**Síntoma:** Importaciones que parecen lógicas (`from fastapi import AwesomeAuth`) pero no existen o cambiaron en la versión actual.
**Auditoría:**
- [ ] ¿Pasa el `uv sync` sin errores?
- [ ] ¿Has verificado en PyPI que el paquete tiene mantenimiento activo en 2026?

## 3. Comentarios "Loro" (Parrot Comments)
**Síntoma:** Comentarios que narran lo obvio.
- *Mal:* `x = x + 1 # Incrementa x`
- *Bien:* `x = x + 1 # Ajuste por error de indexación en la librería legacy`
**Auditoría:**
- [ ] Borrar comentarios redundantes generados por la IA.

## 4. Complejidad Ciclomática Escondida
**Síntoma:** La IA genera funciones de 100 líneas con 5 if/else anidados porque "funcionó a la primera".
**Auditoría:**
- [ ] Aplicar principio de Responsabilidad Única.
- [ ] **Acción:** Pídele al agente: "Extrae la lógica de validación a una función pura separada".

## 5. Security by Obscurity
**Síntoma:** Hardcoding de credenciales o lógica de seguridad débil sugerida por ejemplos antiguos.
**Auditoría:**
- [ ] Buscar `api_key = "..."` en el código.
- [ ] Verificar inyección SQL/XSS incluso si el código "se ve limpio".
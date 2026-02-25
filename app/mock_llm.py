# app/mock_llm.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import time

# Un mini-servidor que simula ser OpenAI
mock_app = FastAPI(title="Mock OpenAI Service")

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7

# Simulación de memoria en memoria (se borra al reiniciar)
CONVERSATION_HISTORY = {}

@mock_app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    last_msg = request.messages[-1].content.lower()
    
    # Detección básica de intención "Agentica"
    if "plan" in last_msg:
        content = """Entendido. Aquí está el plan de ejecución (Simulado GPT-5.3):
1. Analizar requisitos.
2. Crear archivo de pruebas.
3. Implementar código.
¿Procedo?"""
    elif "test" in last_msg or "prueba" in last_msg:
        content = "Generando tests con pytest... (Simulación: Se han creado 3 tests unitarios cubriendo edge cases)."
    elif "refactor" in last_msg:
        content = "He detectado complejidad ciclomática alta. Dividiendo la función en tres componentes más pequeños..."
    else:
        # Fallback genérico
        content = f"Simulación GPT-5.3 (Mock): Recibí tu input '{last_msg[:15]}...'. Configura tu API Key real para lógica compleja."

    return {
        "id": "chatcmpl-mock-123",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": content
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(last_msg),
            "completion_tokens": len(content),
            "total_tokens": len(last_msg) + len(content)
        }
    }
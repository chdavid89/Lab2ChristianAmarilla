# app/mock_llm.py
from fastapi import FastAPI, Request
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

@mock_app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Simula una respuesta de OpenAI basada en reglas simples (Heurística)."""
    
    last_msg = request.messages[-1].content.lower()
    
    # Respuestas "Golden Set" predeterminadas para tests
    if "test_connection" in last_msg:
        content = "Conexión exitosa con el Mock LLM."
    elif "sql" in last_msg:
        content = "SELECT * FROM users WHERE active = 1;"
    elif "python" in last_msg:
        content = "def hello_world():\n    print('Hello AI')"
    else:
        content = f"Soy un Mock LLM. Recibí tu mensaje: '{last_msg[:20]}...'. Para respuestas reales, configura tu API Key."

    # Simulamos la estructura de respuesta real de OpenAI
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
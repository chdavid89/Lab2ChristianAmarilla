# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Metadatos para la documentación automática (OpenAPI)
app = FastAPI(
    title="AI Diplomado API",
    description="API Backend para el Diplomado de IA Aplicada a Ingeniería de Software",
    version="0.1.0",
)

# Configuración de CORS (Permite que Streamlit/React se comuniquen con esto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción esto se restringe, para clase es OK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos (Pydantic) ---
class HealthResponse(BaseModel):
    status: str
    version: str
    module: str

# --- Endpoints ---
@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz para verificar que la API respira."""
    return {"message": "Bienvenido a la API del Diplomado AI"}

@app.get("/health", response_model=HealthResponse, tags=["Ops"])
async def health_check():
    """Health check estándar para monitoreo."""
    return HealthResponse(
        status="ok",
        version="0.1.0",
        module="System"
    )

# Aquí agregaremos más adelante los routers:
# app.include_router(agent_router) 

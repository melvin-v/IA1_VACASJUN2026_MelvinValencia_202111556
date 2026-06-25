"""
Punto de entrada de la API REST de RoboMaze.

Configura la aplicación FastAPI, el middleware de CORS (para que el
frontend Vue pueda consumir la API desde otro origen/puerto) y monta
las rutas.

Ejecutar en desarrollo:
    uvicorn app.main:app --reload --port 8000

Documentación interactiva (Swagger):  http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="RoboMaze API",
    description=(
        "API REST para resolver laberintos con algoritmos de búsqueda "
        "(BFS y DFS). Práctica 4 - Inteligencia Artificial 1, USAC."
    ),
    version="1.0.0",
)

# CORS: permite que el frontend (Vue, normalmente en :5173 o :8080) consuma
# la API. En producción conviene restringir allow_origins a los dominios reales.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["root"])
def root() -> dict:
    """Redirección informativa hacia la documentación."""
    return {
        "message": "RoboMaze API. Visita /docs para la documentación interactiva.",
        "health": "/api/health",
    }

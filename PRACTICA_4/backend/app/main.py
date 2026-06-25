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

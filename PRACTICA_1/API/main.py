from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.rutas_controller import router

app = FastAPI(
    title="Sistema de Rutas - Departamentos de Guatemala",
    description=(
        "API REST que utiliza Prolog como motor de inferencia logica "
        "para encontrar rutas optimas entre departamentos de Guatemala."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "mensaje": "API de rutas Guatemala activa",
        "docs": "/docs",
        "endpoints_principales": [
            "GET  /api/ciudades",
            "GET  /api/ruta/corta?origen=X&destino=Y",
            "GET  /api/ruta/todas?origen=X&destino=Y",
            "POST /api/ciudades",
            "POST /api/conexiones",
        ],
    }
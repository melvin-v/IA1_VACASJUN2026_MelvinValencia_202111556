from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.diagnostico_controller import router

app = FastAPI(
    title="Doctor Byte API",
    description="Sistema experto para el diagnostico de fallas en computadoras.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/", tags=["General"])
def raiz():
    return {"servicio": "Doctor Byte API", "estado": "activo", "docs": "/docs"}

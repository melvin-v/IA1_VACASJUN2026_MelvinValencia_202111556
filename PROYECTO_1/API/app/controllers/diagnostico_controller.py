from fastapi import APIRouter

from app.controllers.dependencias import obtener_servicio
from app.schemas.diagnostico_schema import (
    DiagnosticoRequest,
    DiagnosticoResponse,
    SintomaOut,
)

router = APIRouter()

# Instancia unica del Service (con su Repository ya inyectado).
_servicio = obtener_servicio()


@router.get("/sintomas", response_model=list[SintomaOut], tags=["Sintomas"])
def obtener_sintomas():
    """Devuelve el catalogo completo de sintomas disponibles."""
    return _servicio.listar_sintomas()


@router.post("/diagnostico", response_model=DiagnosticoResponse, tags=["Diagnostico"])
def generar_diagnostico(peticion: DiagnosticoRequest):
    """Recibe una lista de sintomas y devuelve las fallas diagnosticadas."""
    return _servicio.diagnosticar(peticion.sintomas)

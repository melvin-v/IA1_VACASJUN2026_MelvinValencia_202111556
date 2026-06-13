from fastapi import APIRouter

from app.controllers.dependencias import obtener_servicio
from app.schemas.diagnostico_schema import (
    DiagnosticoRequest,
    DiagnosticoResponse,
    SintomaOut,
)
from app.schemas.historial_schema import HistorialItem

router = APIRouter()

_servicio = obtener_servicio()


@router.get("/sintomas", response_model=list[SintomaOut], tags=["Sintomas"])
def obtener_sintomas():
    """Devuelve el catalogo completo de sintomas disponibles."""
    return _servicio.listar_sintomas()


@router.post("/diagnostico", response_model=DiagnosticoResponse, tags=["Diagnostico"])
def generar_diagnostico(peticion: DiagnosticoRequest):
    """Recibe una lista de sintomas y devuelve las fallas diagnosticadas."""
    return _servicio.diagnosticar(peticion.sintomas)


@router.get("/historial", response_model=list[HistorialItem], tags=["Historial"])
def obtener_historial(limite: int | None = None):
    """Devuelve los diagnosticos realizados, los mas recientes primero.

    Parametro opcional 'limite' para traer solo los N mas recientes.
    """
    return _servicio.listar_historial(limite)
